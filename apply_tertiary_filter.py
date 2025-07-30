import itertools
from imd3 import calcRating, loadVtxTable, getFrequencyWithChannel
import argparse

def read_ranking_from_file(filename="secondary_ranking.txt"):
    """二次合成の順位リストをファイルから読み込む"""
    results = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line.startswith('-') or not line:
                    continue
                
                # 形式: 順位, 周波数1(チャネル), 周波数2(チャネル), 周波数3(チャネル), 周波数4(チャネル), 評価値
                parts = line.split(',')
                if len(parts) >= 6:
                    rank = int(parts[0].strip())
                    
                                    # チャネル名とLED番号を除去して周波数のみを抽出
                frequencies = []
                for f in parts[1:5]:
                    freq_str = f.strip()
                    # (チャネル)周波数[LED番号] の形式から周波数のみを抽出
                    if '(' in freq_str and ')' in freq_str:
                        # (E2)5685[LED3] のような形式から 5685 を抽出
                        freq_str = freq_str.split(')')[-1]
                    # [LED番号] を除去
                    if '[' in freq_str:
                        freq_str = freq_str.split('[')[0]
                    frequencies.append(int(freq_str))
                    
                    secondary_rating = int(parts[5].strip())
                    results.append((rank, frequencies, secondary_rating))
    except FileNotFoundError:
        print(f"エラー: {filename} が見つかりません")
        return []
    except ValueError as e:
        print(f"エラー: ファイルの形式が正しくありません: {e}")
        return []
    
    return results

def check_imd_differences(frequencies, threshold=20):
    """imd3.pyのcalcRatingルーチン内で計算されるdifferenceをチェック（20MHz未満を排除対象）"""
    from imd3 import calcRating
    
    # calcRatingの内部ロジックを模倣してdifferenceを計算
    n = len(frequencies)
    differences = []
    
    for row in range(n):
        for column in range(n):
            if row == column:
                continue
            
            # 二次合成
            thirdFrequency = frequencies[row] * 2 - frequencies[column]
            if thirdFrequency >= 5100 and thirdFrequency <= 6099:  # isValidFrequency
                nearest = min(frequencies, key=lambda f: abs(f - thirdFrequency))
                difference = abs(thirdFrequency - nearest)
                if difference < threshold:  # 20MHz未満
                    differences.append((thirdFrequency, nearest, difference, f"二次合成: f{row+1}*2 - f{column+1}"))
            
            # 三次合成パターン（10パターン）
            for k in range(n):
                if k == row or k == column:
                    continue
                
                # パターン1: f1 - f2 + f3
                third_order = frequencies[row] - frequencies[column] + frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン1): f{row+1} - f{column+1} + f{k+1}"))
                
                # パターン2: f1 + f2 - f3
                third_order = frequencies[row] + frequencies[column] - frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン2): f{row+1} + f{column+1} - f{k+1}"))
                
                # パターン3: 2*f1 - f2 - f3
                third_order = 2 * frequencies[row] - frequencies[column] - frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン3): 2*f{row+1} - f{column+1} - f{k+1}"))
                
                # パターン4: f1 + f2 + f3
                third_order = frequencies[row] + frequencies[column] + frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン4): f{row+1} + f{column+1} + f{k+1}"))
                
                # パターン5: -f1 + f2 + f3
                third_order = -frequencies[row] + frequencies[column] + frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン5): -f{row+1} + f{column+1} + f{k+1}"))
                
                # パターン6: 2*f1 + f2 - f3
                third_order = 2 * frequencies[row] + frequencies[column] - frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン6): 2*f{row+1} + f{column+1} - f{k+1}"))
                
                # パターン7: 2*f1 - f2 + f3
                third_order = 2 * frequencies[row] - frequencies[column] + frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン7): 2*f{row+1} - f{column+1} + f{k+1}"))
                
                # パターン8: f1 - 2*f2 + f3
                third_order = frequencies[row] - 2 * frequencies[column] + frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン8): f{row+1} - 2*f{column+1} + f{k+1}"))
                
                # パターン9: f1 + 2*f2 - f3
                third_order = frequencies[row] + 2 * frequencies[column] - frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン9): f{row+1} + 2*f{column+1} - f{k+1}"))
                
                # パターン10: -f1 + 2*f2 + f3
                third_order = -frequencies[row] + 2 * frequencies[column] + frequencies[k]
                if third_order >= 5100 and third_order <= 6099:
                    nearest = min(frequencies, key=lambda f: abs(f - third_order))
                    difference = abs(third_order - nearest)
                    if difference < threshold:
                        differences.append((third_order, nearest, difference, f"三次合成(パターン10): -f{row+1} + 2*f{column+1} + f{k+1}"))
    
    return differences

def apply_tertiary_evaluation_and_filter(ranking_results, imd_diff_threshold=20):
    """三次合成による評価を行い、IMD差閾値未満の印を付ける（重複排除付き）"""
    vtx_table = loadVtxTable()
    filtered_results = []
    seen = set()  # 重複排除用セット
    
    print(f"三次合成による評価とIMD差{imd_diff_threshold}MHz未満チェックを実行中...")
    print("-" * 80)
    
    for rank, frequencies, secondary_rating in ranking_results:
        # 周波数セット（順不同）で重複排除
        freq_key = tuple(sorted(frequencies))
        if freq_key in seen:
            continue
        seen.add(freq_key)
        
        # 三次合成による評価
        tertiary_rating = calcRating(frequencies)
        
        # IMD differenceチェック（閾値未満を排除対象）
        imd_differences = check_imd_differences(frequencies, threshold=imd_diff_threshold)
        
        # 結果を記録
        result = {
            'rank': rank,
            'frequencies': frequencies,
            'secondary_rating': secondary_rating,
            'tertiary_rating': tertiary_rating,
            'imd_differences': imd_differences,
            'should_exclude': len(imd_differences) > 0
        }
        
        filtered_results.append(result)
        
        # 上位20件の詳細を表示
        if rank <= 20:
            freq_with_channel = [getFrequencyWithChannel(f, vtx_table) for f in frequencies]
            print(f"{rank:3d}. 周波数: {freq_with_channel}")
            print(f"    二次合成評価: {secondary_rating}, 三次合成評価: {tertiary_rating}")
            
            if imd_differences:
                print(f"    ⚠️  IMD差{imd_diff_threshold}MHz未満検出: ", end="")
                for third_freq, nearest, diff, pattern in imd_differences[:3]:  # 最初の3つまで表示
                    print(f"({pattern}: {third_freq}-{nearest}={diff}MHz) ", end="")
                if len(imd_differences) > 3:
                    print(f"...他{len(imd_differences)-3}件 ", end="")
                print("→ 排除対象")
            else:
                print(f"    ✅ IMD差{imd_diff_threshold}MHz未満なし → 採用候補")
            print()
    
    return filtered_results

def save_filtered_results(results, filename="filtered_ranking.txt"):
    """フィルタリング結果をファイルに保存"""
    vtx_table = loadVtxTable()
    
    # LEDテーブルを読み込み
    def load_led_table():
        """LED.txtから周波数レンジとLED数値の対応関係を読み込む"""
        led_ranges = []
        try:
            with open('LED.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        range_str = parts[0]
                        led_number = int(parts[2])
                        range_parts = range_str.split(' <= ')
                        if len(range_parts) == 2:
                            min_freq = int(range_parts[0])
                            max_freq = int(range_parts[1])
                            led_ranges.append((min_freq, max_freq, led_number))
        except FileNotFoundError:
            print("警告: LED.txtが見つかりません")
        return led_ranges
    
    def get_led_number(frequency, led_ranges):
        """周波数に対応するLED数値を取得"""
        for min_freq, max_freq, led_number in led_ranges:
            if min_freq <= frequency <= max_freq:
                return led_number
        return None
    
    led_ranges = load_led_table()
    
    with open(filename, 'w') as f:
        f.write("# 三次合成評価とIMD差フィルタリング結果\n")
        f.write("# 形式: 順位, 周波数1(チャネル)[LED], 周波数2(チャネル)[LED], 周波数3(チャネル)[LED], 周波数4(チャネル)[LED], 二次合成評価, 三次合成評価, 排除フラグ, IMD差詳細\n")
        f.write("-" * 140 + "\n")
        
        for result in results:
            # 周波数にチャネル名とLED番号を付けて表示
            freq_with_channel_led = []
            led_numbers = []
            for freq in result['frequencies']:
                channel_str = getFrequencyWithChannel(freq, vtx_table)
                led_num = get_led_number(freq, led_ranges)
                if led_num is not None:
                    freq_with_channel_led.append(f"{channel_str}[LED{led_num}]")
                    led_numbers.append(led_num)
                else:
                    freq_with_channel_led.append(f"{channel_str}[LED?]")
                    led_numbers.append(None)
            
            freq_str = ", ".join(freq_with_channel_led)
            
            # LED番号の重複チェック
            valid_led_numbers = [led for led in led_numbers if led is not None]
            led_safe = len(valid_led_numbers) == 4 and len(set(valid_led_numbers)) == 4
            
            exclude_flag = "EXCLUDE" if result['should_exclude'] else "KEEP"
            if not result['should_exclude'] and led_safe:
                exclude_flag = "KEEP LED safe"
            
            imd_details = ""
            if result['imd_differences']:
                imd_details = "; ".join([f"{pattern}: {third_freq}-{nearest}={diff}MHz" for third_freq, nearest, diff, pattern in result['imd_differences']])
            
            f.write(f"{result['rank']:4d}, {freq_str}, {result['secondary_rating']}, {result['tertiary_rating']}, {exclude_flag}, {imd_details}\n")
    
    print(f"フィルタリング結果を {filename} に保存しました")

def print_summary(results):
    """結果のサマリーを表示"""
    total = len(results)
    excluded = sum(1 for r in results if r['should_exclude'])
    kept = total - excluded
    
    print("-" * 80)
    print("フィルタリング結果サマリー:")
    print(f"総組み合わせ数: {total}")
    print(f"排除対象: {excluded} (IMD差20MHz未満)")
    print(f"採用候補: {kept}")
    print(f"排除率: {excluded/total*100:.1f}%")
    
    # 採用候補の上位10件を表示
    print("\n採用候補（IMD差20MHz未満なし）の上位10件:")
    print("-" * 80)
    
    kept_results = [r for r in results if not r['should_exclude']]
    for i, result in enumerate(kept_results[:10], 1):
        freq_with_channel = [getFrequencyWithChannel(f, loadVtxTable()) for f in result['frequencies']]
        print(f"{i:2d}. 元順位{result['rank']:3d}: {freq_with_channel}")
        print(f"    二次合成評価: {result['secondary_rating']}, 三次合成評価: {result['tertiary_rating']}")

def main():
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description="三次合成IMD差フィルタリング")
    parser.add_argument('--imd-diff-threshold', type=int, default=20, help='IMD差フィルタの閾値（MHz未満で排除, デフォルト: 20）')
    args = parser.parse_args()
    imd_diff_threshold = args.imd_diff_threshold

    # 二次合成の順位リストを読み込み
    ranking_results = read_ranking_from_file()
    
    if not ranking_results:
        print("エラー: 順位リストを読み込めませんでした")
        return
    
    # 三次合成による評価とフィルタリング
    filtered_results = apply_tertiary_evaluation_and_filter(ranking_results, imd_diff_threshold)
    
    # 結果をファイルに保存
    save_filtered_results(filtered_results)
    
    # サマリーを表示
    print_summary(filtered_results)

if __name__ == "__main__":
    main() 