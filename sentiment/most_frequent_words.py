"""
This script provides most frequent positive and negative words in the processed relevant ESG sentences.
"""

from pathlib import Path
import time
import json
from collections import defaultdict

t = time.time()

report_sentiment_words_path = Path("reports") / "report_sentiment_words.json"

with open(report_sentiment_words_path, "r") as json_file:
    report_sentiment_words = json.load(json_file)

all_positives = defaultdict(int)
all_negatives = defaultdict(int)
for comp, reports in report_sentiment_words.items():
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
