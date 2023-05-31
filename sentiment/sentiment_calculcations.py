"""
This script provides descriptive statistics on the counts of positive and negative words in the processed relevant ESG sentences.
It also calculates the first sentiment polarity index.
"""

from pathlib import Path
import time
import numpy as np
import pandas as pd
import json

t = time.time()

report_stats_path = Path("reports") / "report_stats.json"

with open(report_stats_path, "r") as json_file:
    report_stats = json.load(json_file)

n_positives = np.array([c[r]["n_positive_words"] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(n_positives, columns=["lengths"]).describe())

n_negatives = np.array([c[r]["n_negative_words"] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(n_negatives, columns=["lengths"]).describe())

sentiment_polarity = np.array(
    [
        (c[r]["n_positive_words"] - c[r]["n_negative_words"]) / (c[r]["n_positive_words"] + c[r]["n_negative_words"])
        for c in report_stats.values()
        for r in c.keys()
    ]
)
print(pd.DataFrame(sentiment_polarity, columns=["lengths"]).describe())
