#!/usr/bin/env python3

import argparse
import os
import json
import matplotlib.pyplot as plt
import re
from collections import defaultdict

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True, help="List of hashtags to track")
parser.add_argument('--input_folder', required=True, help="Path to folder containing output files")
parser.add_argument('--output_path', default="trend_plot.png", help="Output image file name")
args = parser.parse_args()

# Dictionary to store hashtag trends over time
hashtag_counts = defaultdict(lambda: defaultdict(int))

# Regex to extract the date from filenames (e.g., geoTwitter20-01-01.lang)
date_pattern = re.compile(r'geoTwitter(\d{2})-(\d{2})-(\d{2})')

# Read all .lang files in the input folder
all_dates = set()

for filename in sorted(os.listdir(args.input_folder)):
    if filename.endswith('.lang'):
        match = date_pattern.search(filename)
        if match:
            year, month, day = match.groups()
            date_str = f"20{year}-{month}-{day}"  # Construct YYYY-MM-DD format
            all_dates.add(date_str)

            # Load JSON data
            try:
                with open(os.path.join(args.input_folder, filename)) as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Skipping {filename} due to error: {e}")
                continue

            # Store counts for requested hashtags
            for hashtag in args.hashtags:
                hashtag_counts[hashtag][date_str] = sum(data.get(hashtag, {}).values())

# Ensure all dates have entries (fill missing dates with 0)
for hashtag in args.hashtags:
    for date in sorted(all_dates):
        if date not in hashtag_counts[hashtag]:
            hashtag_counts[hashtag][date] = 0

# Plot the data
plt.figure(figsize=(12, 6))

if not hashtag_counts:
    print("No valid data found for the given hashtags.")
    exit()

for hashtag, counts in hashtag_counts.items():
    dates = sorted(counts.keys())  # Sort dates chronologically
    values = [counts[date] for date in dates]

    plt.plot(dates, values, linestyle='-', label=hashtag)  # Removed marker='o'

# Format plot
plt.xlabel("Date")
plt.ylabel("Number of Tweets")
plt.title("Hashtag Trends Over Time")

if dates:
    select_dates = dates[::max(1, len(dates) // 10)]
    plt.xticks(select_dates, rotation=45, fontsize=8)

plt.legend()
plt.tight_layout()

# Save plot
plt.savefig(args.output_path)
print(f"Plot saved to {args.output_path}")

