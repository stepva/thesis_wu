"""
This script provides most frequent positive and negative words in the sentimented NEWS or REPORTS.
"""

from pathlib import Path
import time
import json
from collections import defaultdict

REPORTS = False
NEWS = True
assert not (REPORTS and NEWS)

t = time.time()

if REPORTS:
    sentiment_words_path = Path("reports") / "report_sentiment_words.json"
    print("ANALYZING REPORTS")
else:
    sentiment_words_path = Path("news") / "news_sentiment_words.json"
    print("ANALYZING NEWS")

with open(sentiment_words_path, "r") as json_file:
    sentiment_words = json.load(json_file)

all_positives = defaultdict(int)
all_negatives = defaultdict(int)
for comp, reports in sentiment_words.items():
    for rep, words in reports.items():
        for k, v in words["positive_words"].items():
            all_positives[k] += v
        for k, v in words["negative_words"].items():
            all_negatives[k] += v

all_positives = [(k, v) for k, v in sorted(all_positives.items(), key=lambda item: item[1], reverse=True)]
print("Unique positive words:", len(all_positives))
print(all_positives[:10])

all_negatives = [(k, v) for k, v in sorted(all_negatives.items(), key=lambda item: item[1], reverse=True)]
print("Unique negative words:", len(all_negatives))
print(all_negatives[:10])
