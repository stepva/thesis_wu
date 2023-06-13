"""
This script checks the sentiment-ready processed files for length of sentences.
Note that there seem to be some strangely processed long sentences, which might be removed for the sentiment analysis itself.
"""

from pathlib import Path
import numpy as np
import pandas as pd

from data_processing.utils import list_folders, list_files

sentiment_ready = Path("reports") / "sentiment_ready"

min_lengths = []
avg_lengths = []
max_lengths = []
all_lengths = []

for company in list_folders(sentiment_ready):
    for report in list_files(sentiment_ready / company):
        esg_txt = sentiment_ready / company / report
        with open(esg_txt, "r") as file:
            sentences = file.readlines()
            sentences = [s.rstrip().split() for s in sentences]
            lengths = [len(s) for s in sentences]
            min_lengths.append(min(lengths))
            avg_lengths.append(np.mean(lengths))
            max_lengths.append(max(lengths))
            all_lengths += lengths

# print(pd.DataFrame(np.array(min_lengths), columns=['min']).describe())
print(pd.DataFrame(np.array(avg_lengths), columns=["avg"]).quantile([0.01, 0.025, 0.975, 0.99]))
# print(pd.DataFrame(np.array(max_lengths), columns=['max']).describe())
print(
    pd.DataFrame(np.array(all_lengths), columns=["all"]).quantile([0.01, 0.025, 0.975, 0.98, 0.985, 0.99, 0.995, 0.999])
)

# min - doesn't make sense to have one-word sentence, make it >= 2
# some stences doesn't make sense and are probably weirdly processed tables or so, especially long ones
# I would like to cut the long sentences, probably <= 100
# theoretically the issue is not in the length, there might be some important information,
# but if I were to calculate the sentiment using the ratio to total words, this would skew it a lot
