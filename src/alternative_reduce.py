#!/usr/bin/env python3

import argparse
import os
import json
from collections import defaultdict
import re
import matplotlib.pyplot as plt

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True, help="List of JSON files to process")
parser.add_argument('--hashtags', nargs='+', required=True, help="List of hashtags to analyze")
args = parser.parse_args()

# Helper function to extract date from filename
def extract_date_pattern(filename):
    match = re.search(r'(\d{2})-(\d{2})-(\d{2})', filename)
    return match.group(0) if match else None  # Returns "MM-DD-YY" or None if not found

# Data storage
total = defaultdict(lambda: defaultdict(int))

# Read and process each JSON file
for path in args.input_paths:
    date = extract_date_pattern(os.path.basename(path))  # Ensure we're extracting correctly
    if date:
        with open(path, 'r') as f:
            data = json.load(f)

        # Aggregate hashtag counts for each date
        for hashtag in args.hashtags:
            if hashtag in data:
                total[date][hashtag] = sum(data[hashtag].values())

# Debugging: Print extracted data
print("Extracted Data:")
for date, counts in total.items():
    print(f"{date}: {counts}")

# Sort dates to ensure correct chronological order
dates = sorted(total.keys(), key=lambda x: tuple(map(int, x.split('-'))))  # Sort by MM-DD-YY

# Prepare plot data
hashtag_counts = {tag: [total[date].get(tag, 0) for date in dates] for tag in args.hashtags}

# Debugging: Check final data
print("Final Data for Plotting:")
for tag, counts in hashtag_counts.items():
    print(f"{tag}: {counts}")

# Plot the data
plt.figure(figsize=(12, 6))

for tag, counts in hashtag_counts.items():
    plt.plot(dates, counts, marker='o', label=tag)

# Formatting
plt.xlabel("Date")
plt.ylabel("Number of Tweets")
plt.title("Hashtag Frequency Over Time")
plt.xticks(rotation=45, fontsize=8)  # Rotate date labels

# Reduce number of x-axis labels for readability
plt.xticks(dates[::max(1, len(dates) // 20)], rotation=45, fontsize=8)

plt.legend()
plt.grid(True)

# Generate a unique filename based on hashtags
safe_hashtags = "_".join([re.sub(r"[^\w]", "", tag) for tag in args.hashtags])
output_filename = f"hashtag_trend_{safe_hashtags}.png"
plt.savefig(output_filename, dpi=300, bbox_inches="tight")
print(f"Plot saved as {output_filename}")

# Close plot to free memory
plt.close()

