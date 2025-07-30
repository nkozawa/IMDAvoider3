import itertools
from imd import calcRating

def read_frequencies_from_file(filename):
    """freq.txtファイルから周波数を読み込む"""
    frequencies = []
    with open(filename, 'r') as f:
        for line in f:
            # 各行の周波数を整数として読み込み
            line_freqs = [int(freq) for freq in line.strip().split()]
            frequencies.extend(line_freqs)
    return frequencies

def create_secondary_ranking(frequencies):
    """全ての4周波数の組み合わせで二次合成による評価を行い、順位リストを作成"""
    # 重複を除去してソート
    unique_frequencies = sorted(list(set(frequencies)))
    
    print(f"読み込まれた周波数: {unique_frequencies}")
    print(f"総周波数数: {len(unique_frequencies)}")
    print(f"4周波数の組み合わせ数: {len(list(itertools.combinations(unique_frequencies, 4)))}")
    print("-" * 80)
    
    results = []
    
    # 全ての4周波数の組み合わせを生成
    for combo in itertools.combinations(unique_frequencies, 4):
        rating = calcRating(list(combo))
        results.append((list(combo), rating))
    
    # 評価値でソート（降順）
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

def save_ranking_to_file(results, filename="secondary_ranking.txt"):
    """順位リストをファイルに保存"""
    from imd3 import loadVtxTable, getFrequencyWithChannel
    
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
        f.write("# 二次合成による4周波数組み合わせ順位リスト\n")
        f.write("# 形式: 順位, 周波数1(チャネル)[LED], 周波数2(チャネル)[LED], 周波数3(チャネル)[LED], 周波数4(チャネル)[LED], 評価値\n")
        f.write("-" * 120 + "\n")
        
        for i, (combo, rating) in enumerate(results, 1):
            # 周波数にチャネル名とLED番号を付けて表示
            freq_with_channel_led = []
            for freq in combo:
                channel_str = getFrequencyWithChannel(freq, vtx_table)
                led_num = get_led_number(freq, led_ranges)
                if led_num is not None:
                    freq_with_channel_led.append(f"{channel_str}[LED{led_num}]")
                else:
                    freq_with_channel_led.append(f"{channel_str}[LED?]")
            
            freq_str = ", ".join(freq_with_channel_led)
            f.write(f"{i:4d}, {freq_str}, {rating}\n")
    
    print(f"順位リストを {filename} に保存しました")

def main():
    # freq.txtから周波数を読み込み
    frequencies = read_frequencies_from_file('freq.txt')
    
    # 二次合成による評価と順位リスト作成
    results = create_secondary_ranking(frequencies)
    
    # 結果を表示
    print("二次合成による4周波数組み合わせの評価結果（評価値順）:")
    print("-" * 80)
    
    for i, (combo, rating) in enumerate(results[:20], 1):  # 上位20件を表示
        print(f"{i:3d}. 周波数: {combo} -> 評価値: {rating}")
    
    print("-" * 80)
    print(f"総組み合わせ数: {len(results)}")
    
    # 最高評価値の組み合わせを強調表示
    if results:
        best_combo, best_rating = results[0]
        print(f"\n最高評価値: {best_rating}")
        print(f"最適な4周波数組み合わせ: {best_combo}")
    
    # 順位リストをファイルに保存
    save_ranking_to_file(results)
    
    return results

if __name__ == "__main__":
    main() 