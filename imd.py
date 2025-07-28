MIN_DISPLAY_FREQUENCY = 5100
MAX_DISPLAY_FREQUENCY = 6099
RATING_MAX_VALUE = 100
RATING_DIFF_LIMIT = 35


def loadVtxTable():
    """vtxtable.txtから周波数とチャネルの対応関係を読み込む"""
    frequency_to_channel = {}
    try:
        with open('vtxtable.txt', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 9:  # バンド名、周波数が含まれている行
                    band_letter = parts[4]  # A, B, E, F, R
                    frequencies = parts[6:]  # 周波数のリスト
                    
                    for i, freq in enumerate(frequencies):
                        try:
                            freq_int = int(freq)
                            channel_name = f"{band_letter}{i+1}"
                            frequency_to_channel[freq_int] = channel_name
                        except ValueError:
                            continue
    except FileNotFoundError:
        print("警告: vtxtable.txtが見つかりません")
    return frequency_to_channel


def getFrequencyWithChannel(frequency: int, vtx_table: dict):
    """周波数にチャネル名を付けて返す"""
    if frequency in vtx_table:
        return f"({vtx_table[frequency]}){frequency}"
    else:
        return str(frequency)


def isValidFrequency(frequency: int):
    return MIN_DISPLAY_FREQUENCY <= frequency <= MAX_DISPLAY_FREQUENCY


def findNearestFrequency(frequency: int, frequencies: list):
    nearest = frequencies[0]
    for f in frequencies:
        if abs(f - frequency) < abs(nearest - frequency):
            nearest = f
    return nearest


def calcRating(frequencies: list, debug: bool = False):
    vtx_table = loadVtxTable()
    n = len(frequencies)
    total = 0
    for row in range(n):
        for column in range(n):
            if row == column:
                continue
            # 二次合成
            thirdFrequency = frequencies[row] * 2 - frequencies[column]
            if isValidFrequency(thirdFrequency):
                nearest = findNearestFrequency(thirdFrequency, frequencies)
                difference = abs(thirdFrequency - nearest)
                if difference <= RATING_DIFF_LIMIT:
                    value = RATING_DIFF_LIMIT - difference
                    if debug:
                        print(f"二次合成: f{row+1}*2 - f{column+1} = {getFrequencyWithChannel(frequencies[row], vtx_table)}*2 - {getFrequencyWithChannel(frequencies[column], vtx_table)} = {getFrequencyWithChannel(thirdFrequency, vtx_table)}")
                        print(f"  対象周波数: {getFrequencyWithChannel(thirdFrequency, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                        print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                    total += value * value
            
            # 三次合成パターン
            # 考えられる三次合成パターン:
            # 1. f1 - f2 + f3 (現在実装済み)
            # 2. f1 + f2 - f3
            # 3. 2*f1 - f2 - f3
            # 4. f1 + f2 + f3
            # 5. -f1 + f2 + f3
            # 6. 2*f1 + f2 - f3
            # 7. 2*f1 - f2 + f3
            # 8. f1 - 2*f2 + f3
            # 9. f1 + 2*f2 - f3
            # 10. -f1 + 2*f2 + f3
            
            for k in range(n):
                if k == row or k == column:
                    continue
                
                # パターン1: f1 - f2 + f3 (現在実装済み)
                third_order = frequencies[row] - frequencies[column] + frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン1): f{row+1} - f{column+1} + f{k+1} = {getFrequencyWithChannel(frequencies[row], vtx_table)} - {getFrequencyWithChannel(frequencies[column], vtx_table)} + {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン2: f1 + f2 - f3
                third_order = frequencies[row] + frequencies[column] - frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン2): f{row+1} + f{column+1} - f{k+1} = {getFrequencyWithChannel(frequencies[row], vtx_table)} + {getFrequencyWithChannel(frequencies[column], vtx_table)} - {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン3: 2*f1 - f2 - f3
                third_order = 2 * frequencies[row] - frequencies[column] - frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン3): 2*f{row+1} - f{column+1} - f{k+1} = 2*{getFrequencyWithChannel(frequencies[row], vtx_table)} - {getFrequencyWithChannel(frequencies[column], vtx_table)} - {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン4: f1 + f2 + f3
                third_order = frequencies[row] + frequencies[column] + frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン4): f{row+1} + f{column+1} + f{k+1} = {getFrequencyWithChannel(frequencies[row], vtx_table)} + {getFrequencyWithChannel(frequencies[column], vtx_table)} + {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン5: -f1 + f2 + f3
                third_order = -frequencies[row] + frequencies[column] + frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン5): -f{row+1} + f{column+1} + f{k+1} = -{getFrequencyWithChannel(frequencies[row], vtx_table)} + {getFrequencyWithChannel(frequencies[column], vtx_table)} + {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン6: 2*f1 + f2 - f3
                third_order = 2 * frequencies[row] + frequencies[column] - frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン6): 2*f{row+1} + f{column+1} - f{k+1} = 2*{getFrequencyWithChannel(frequencies[row], vtx_table)} + {getFrequencyWithChannel(frequencies[column], vtx_table)} - {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン7: 2*f1 - f2 + f3
                third_order = 2 * frequencies[row] - frequencies[column] + frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン7): 2*f{row+1} - f{column+1} + f{k+1} = 2*{getFrequencyWithChannel(frequencies[row], vtx_table)} - {getFrequencyWithChannel(frequencies[column], vtx_table)} + {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン8: f1 - 2*f2 + f3
                third_order = frequencies[row] - 2 * frequencies[column] + frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン8): f{row+1} - 2*f{column+1} + f{k+1} = {getFrequencyWithChannel(frequencies[row], vtx_table)} - 2*{getFrequencyWithChannel(frequencies[column], vtx_table)} + {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン9: f1 + 2*f2 - f3
                third_order = frequencies[row] + 2 * frequencies[column] - frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン9): f{row+1} + 2*f{column+1} - f{k+1} = {getFrequencyWithChannel(frequencies[row], vtx_table)} + 2*{getFrequencyWithChannel(frequencies[column], vtx_table)} - {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
                
                # パターン10: -f1 + 2*f2 + f3
                third_order = -frequencies[row] + 2 * frequencies[column] + frequencies[k]
                if isValidFrequency(third_order):
                    nearest = findNearestFrequency(third_order, frequencies)
                    difference = abs(third_order - nearest)
                    if difference <= RATING_DIFF_LIMIT:
                        value = RATING_DIFF_LIMIT - difference
                        if debug:
                            print(f"三次合成(パターン10): -f{row+1} + 2*f{column+1} + f{k+1} = -{getFrequencyWithChannel(frequencies[row], vtx_table)} + 2*{getFrequencyWithChannel(frequencies[column], vtx_table)} + {getFrequencyWithChannel(frequencies[k], vtx_table)} = {getFrequencyWithChannel(third_order, vtx_table)}")
                            print(f"  対象周波数: {getFrequencyWithChannel(third_order, vtx_table)}, 最近接周波数: {getFrequencyWithChannel(nearest, vtx_table)}, 差: {difference}")
                            print(f"  評価値: {RATING_DIFF_LIMIT} - {difference} = {value}")
                        total += value * value
    return round(RATING_MAX_VALUE - total / 5 / n)


if __name__ == "__main__":
    import sys
    
    debug_mode = "--debug" in sys.argv
    
    # コマンドライン引数から周波数を取得
    frequencies = []
    for arg in sys.argv[1:]:
        if arg != "--debug":
            try:
                freq = int(arg)
                frequencies.append(freq)
            except ValueError:
                print(f"エラー: '{arg}' は有効な周波数ではありません")
                sys.exit(1)
    
    # 周波数が指定されていない場合はデフォルト値を使用
    if not frequencies:
        frequencies = [5685, 5725, 5785, 5805]
        print("周波数が指定されていません。デフォルト値を使用します:")
        print(f"周波数: {frequencies}")
    
    # VTXテーブルを読み込んで周波数にバンド名を付けて表示
    vtx_table = loadVtxTable()
    freq_with_band = []
    for freq in frequencies:
        freq_with_band.append(getFrequencyWithChannel(freq, vtx_table))
    
    print(f"評価対象周波数: {freq_with_band}")
    rating = calcRating(frequencies, debug=debug_mode)
    print(f"最終評価: {rating}")

