"""
This script converts the json file with the news statistics to a csv file.
"""

from pathlib import Path
import json
import pandas as pd

with open(Path("news") / "news_stats.json", "r") as json_file:
    news_stats = json.load(json_file)

news_results = pd.DataFrame()

for company, comp_dict in news_stats.items():
    comp_results = pd.DataFrame(comp_dict).T
    comp_results["company"] = company
    comp_results["year"] = comp_results.index
    comp_results.reset_index(inplace=True, drop=True)

    comp_results = comp_results.loc[(comp_results["n_negative_words"] + comp_results["n_positive_words"]) > 0]
    if comp_results.empty:
        continue

    def calc_sentiment_polarity(row):
        return (row["n_positive_words"] - row["n_negative_words"]) / (row["n_positive_words"] + row["n_negative_words"])

    def calc_sentiment_polarity_fy(row):
        if (row["n_negative_words_fy"] + row["n_positive_words_fy"]) > 0:
            return (row["n_positive_words_fy"] - row["n_negative_words_fy"]) / (
                row["n_positive_words_fy"] + row["n_negative_words_fy"]
            )
        else:
            return None

    comp_results["sentiment_polarity"] = comp_results.apply(calc_sentiment_polarity, axis=1)

    if "n_positive_words_fy" in comp_results.columns:
        comp_results["sentiment_polarity_fy"] = comp_results.apply(calc_sentiment_polarity_fy, axis=1)

    news_results = pd.concat([news_results, comp_results])

first_cols = ["company", "year"]
news_results = news_results[first_cols + [c for c in news_results.columns if c not in first_cols]]

news_results["year"] = news_results["year"].astype(int)
news_results.sort_values(by=["company", "year"], inplace=True)

# news_results = news_results.loc[news_results["year"] != 2022]

news_results.to_csv(Path("news") / "news_results.csv", index=False)
