import itertools
from imd import calcRating

def load_led_table():
    """LED.txtから周波数レンジとLED数値の対応関係を読み込む"""
    led_ranges = []
    try:
        with open('LED.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    range_str = parts[0]
                    color = parts[1]
                    led_number = int(parts[2])
                    
                    # レンジ文字列を解析（例: "5100 <= 5672"）
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

def read_frequencies_from_file(filename):
    """freq.txtファイルから周波数を読み込む"""
    frequencies = []
    with open(filename, 'r') as f:
        for line in f:
            # 各行の周波数を整数として読み込み
            line_freqs = [int(freq) for freq in line.strip().split()]
            frequencies.extend(line_freqs)
    return frequencies

def calculate_all_4freq_combinations(frequencies):
    """全ての4周波数の組み合わせでcalRatingを実行"""
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
        results.append((combo, rating))
    
    # 評価値でソート（降順）
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

def main():
    # LED.txtから周波数レンジとLED数値の対応関係を読み込み
    led_ranges = load_led_table()
    
    # freq.txtから周波数を読み込み
    frequencies = read_frequencies_from_file('freq.txt')
    # 全ての4周波数の組み合わせでcalRatingを実行
    results = calculate_all_4freq_combinations(sorted(frequencies))

    # 結果を表示
    print("4周波数組み合わせの評価結果（評価値順）:")
    print("-" * 80)
    
    for i, (combo, rating) in enumerate(results, 1):
        # 各周波数にLED数値を付けて表示
        freq_with_led = []
        for freq in combo:
            led_num = get_led_number(freq, led_ranges)
            if led_num is not None:
                freq_with_led.append(f"{freq}(LED{led_num})")
            else:
                freq_with_led.append(str(freq))
        
        print(f"{i:3d}. 周波数: {freq_with_led} -> 評価値: {rating}")
        
        # 上位10件のみ詳細表示
        if i <= 10:
            print(f"    詳細: {list(combo)}")
    
    print("-" * 80)
    print(f"総組み合わせ数: {len(results)}")
    
    # 最高評価値の組み合わせを強調表示
    if results:
        best_combo, best_rating = results[0]
        # 最高評価の組み合わせにもLED数値を表示
        best_freq_with_led = []
        for freq in best_combo:
            led_num = get_led_number(freq, led_ranges)
            if led_num is not None:
                best_freq_with_led.append(f"{freq}(LED{led_num})")
            else:
                best_freq_with_led.append(str(freq))
        
        print(f"\n最高評価値: {best_rating}")
        print(f"最適な4周波数組み合わせ: {best_freq_with_led}")

if __name__ == "__main__":
    main() 