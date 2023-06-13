"""
This script matches compares the sentimant polarity of reports and news for the same company and year.
Further and more complex pairing of report years with news might be needed due to irregular fiscal report years by some companies.
"""

from pathlib import Path
import time
import json
import numpy as np
import pandas as pd


t = time.time()

report_stats_path = Path("reports") / "report_stats.json"
news_stats_path = Path("news") / "news_stats.json"

with open(report_stats_path, "r") as json_file:
    report_stats = json.load(json_file)

with open(news_stats_path, "r") as json_file:
    news_stats = json.load(json_file)

diffs = []
reps_pols = []
news_pols = []

years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]
for company in report_stats.keys():
    for year in years:
        reports = [r for r in report_stats[company].keys() if year in r]
        if not reports:
            continue
        reps_pos = sum([report_stats[company][r]["n_positive_words"] for r in reports])
        reps_neg = sum([report_stats[company][r]["n_negative_words"] for r in reports])
        reps_pol = (reps_pos - reps_neg) / (reps_pos + reps_neg)

        news_pos = news_stats[company].get(year, {}).get("n_positive_words", -1)
        news_neg = news_stats[company].get(year, {}).get("n_negative_words", -1)
        if news_pos + news_neg < 1:
            continue
        news_pol = (news_pos - news_neg) / (news_pos + news_neg)

        pol_diff = reps_pol - news_pol
        diffs.append(pol_diff)

        reps_pols.append(reps_pol)
        news_pols.append(news_pol)

print(pd.DataFrame(np.array(reps_pols), columns=["reps_pols"]).describe())
print(pd.DataFrame(np.array(news_pols), columns=["news_pols"]).describe())
print(pd.DataFrame(np.array(diffs), columns=["diffs"]).describe())
