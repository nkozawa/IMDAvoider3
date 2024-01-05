MIN_DISPLAY_FREQUENCY = 5100
MAX_DISPLAY_FREQUENCY = 6099
RATING_MAX_VALUE = 100
RATING_DIFF_LIMIT = 35


def isValidFrequency(frequency: int):
    return MIN_DISPLAY_FREQUENCY <= frequency <= MAX_DISPLAY_FREQUENCY


def findNearestFrequency(frequency: int, frequencies: list):
    nearest = frequencies[0]
    for f in frequencies:
        if abs(f - frequency) < abs(nearest - frequency):
            nearest = f
    return nearest


def calcRating(frequencies: list):
    n = len(frequencies)
    total = 0
    for row in range(n):
        for column in range(n):
            if row == column:
                continue
            thirdFrequency = frequencies[row] * 2 - frequencies[column]
            if not isValidFrequency(thirdFrequency):
                continue
            nearest = findNearestFrequency(thirdFrequency, frequencies)
            difference = abs(thirdFrequency - nearest)
            if difference > RATING_DIFF_LIMIT:
                continue
            value = RATING_DIFF_LIMIT - difference
            total += value * value
            # print(f"{row} {column} {thirdFrequency} {nearest} {difference} {value} {total}")
    return round(RATING_MAX_VALUE - total / 5 / n)


if __name__ == "__main__":
    # print(findNearestFrequency(5790, [5760, 5800, 5840]))
    rating = calcRating([5760, 5800, 5840])
    # rating = calcRating([5658, 5695, 5760, 5800, 5880, 5917])
    # rating = calcRating([5658, 5695, 5732, 5769, 5806, 5843, 5880, 5917])
    print(rating)
