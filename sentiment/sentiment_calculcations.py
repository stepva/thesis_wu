"""
This script provides descriptive statistics on the counts of positive and negative words in the processed REPORTS or NEWS.
It also calculates the first sentiment polarity index.
"""

from pathlib import Path
import time
import numpy as np
import pandas as pd
import json

REPORTS = False
NEWS = True
assert not (REPORTS and NEWS)

t = time.time()

if REPORTS:
    stats_path = Path("reports") / "report_stats.json"
    print("ANALYZING REPORTS")
else:
    stats_path = Path("news") / "news_stats.json"
    print("ANALYZING NEWS")

with open(stats_path, "r") as json_file:
    stats = json.load(json_file)

print("Positive words - descriptive stats:")
n_positives = np.array([c[r]["n_positive_words"] for c in stats.values() for r in c.keys()])
print(pd.DataFrame(n_positives, columns=["lengths"]).describe())

print("Negative words - descriptive stats:")
n_negatives = np.array([c[r]["n_negative_words"] for c in stats.values() for r in c.keys()])
print(pd.DataFrame(n_negatives, columns=["lengths"]).describe())

print("Sentiment polarity - descriptive stats:")
sentiment_polarity = np.array(
    [
        (c[r]["n_positive_words"] - c[r]["n_negative_words"]) / (c[r]["n_positive_words"] + c[r]["n_negative_words"])
        for c in stats.values()
        for r in c.keys()
    ]
)
print(pd.DataFrame(sentiment_polarity, columns=["lengths"]).describe())
