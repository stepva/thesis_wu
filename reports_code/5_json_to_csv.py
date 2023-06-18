"""
This script converts the json file with the report stats to a csv file.
"""

from pathlib import Path
import json
import pandas as pd

with open(Path("reports") / "report_stats.json", "r") as json_file:
    report_stats = json.load(json_file)

report_results = pd.DataFrame()

for company, comp_dict in report_stats.items():
    comp_results = pd.DataFrame(comp_dict).T
    comp_results["company"] = company
    comp_results["report"] = comp_results.index
    comp_results.reset_index(inplace=True, drop=True)
    del comp_results["time_taken"]
    comp_results[["year", "additional_info"]] = comp_results["report"].str.extract(r"(\d{4})_?(\w+)?")

    def calc_sentiment_polarity(row):
        return (row["n_positive_words"] - row["n_negative_words"]) / (row["n_positive_words"] + row["n_negative_words"])

    comp_results["sentiment_polarity"] = comp_results.apply(calc_sentiment_polarity, axis=1)

    report_results = pd.concat([report_results, comp_results])

first_cols = ["company", "report", "year", "additional_info"]
report_results = report_results[first_cols + [c for c in report_results.columns if c not in first_cols]]

report_results["year"] = report_results["year"].astype(int)
report_results.sort_values(by=["company", "year"], inplace=True)

report_results = report_results.loc[report_results["year"] != 2022]

report_results.to_csv(Path("reports") / "reports_results.csv", index=False)
