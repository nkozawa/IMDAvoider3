import imd

# Define the ranges and the parameters for the segments we want to find
ranges = [(5690, 5724), (5730, 5754), (5770, 5809)]
segment_width = 9
segments_needed = 4
gap = 1  # Define the minimum gap between segments


# Function to find all the valid segments within a range
def find_segments(range_start, range_end):
    return [start + segment_width // 2 for start in range(range_start, range_end - segment_width + 2)]


# Find all possible segments in all ranges
all_segments = []
for r_start, r_end in ranges:
    all_segments.extend(find_segments(r_start, r_end))


# Function to check if two segments overlap or are too close
def do_segments_overlap(seg1, seg2):
    center_distance = abs(seg1 - seg2)
    return center_distance < segment_width + gap


# Recursive function to find valid combinations of segments
def find_combinations(segments, needed, current_combination=[]):
    if needed == 0:
        return [current_combination]

    if not segments:
        return []

    combinations = []
    for i in range(len(segments)):
        # Check if the current segment overlaps with any segment in the current combination
        if any(do_segments_overlap(segments[i], seg) for seg in current_combination):
            continue
        # Recursive call to find further combinations with the remaining segments
        combinations.extend(find_combinations(segments[i + 1 :], needed - 1, current_combination + [segments[i]]))
    return combinations


# Find all valid combinations of the required number of segments
valid_combinations = find_combinations(all_segments, segments_needed)

# Display the count of combinations and the first 5 combinations for verification
print(f"Total combinations: {len(valid_combinations)}")
# print("First 5 combinations:", valid_combinations[:5])

# calc rating for all combinations
ratings = []
for combination in valid_combinations:
    rating = imd.calcRating(combination)
    ratings.append((rating, combination))
    # print(f"Rating: {rating} - {combination}")

# sort ratings
ratings.sort(key=lambda x: x[0], reverse=True)

# display top 10 ratings
print("Top 10 ratings:")
for rating, combination in ratings[:10]:
    print(f"Rating: {rating} - {combination}")


def drawResults(results):
    import matplotlib.pyplot as plt
    import random

    # Create a new figure
    plt.figure()

    # random_results = random.sample(valid_combinations, 10)

    # Plot the ranges as filled areas
    for i, (r_start, r_end) in enumerate(ranges):
        plt.fill_between([r_start, r_end], -0.5, len(results) - 0.5, color="blue", alpha=0.1)

    # Plot the first 5 valid combinations
    for i, combination in enumerate(results):
        for center in combination:
            seg_start = center - segment_width // 2
            seg_end = center + segment_width // 2
            # print(f"Combination {i + 1}: center={center}, {seg_start} - {seg_end}")
            plt.hlines(i, seg_start, seg_end, colors="blue", linewidth=12)
            plt.text(center, i, str(center), color="white", ha="center", va="center", fontsize=8, weight="bold")

    # Set the labels and the title
    plt.xlabel("Position")
    plt.ylabel("Range / Combination")
    plt.title("Ranges and Valid Combinations")

    # Display the plot
    plt.show()

drawResults([combination for _, combination in ratings[:10]])
