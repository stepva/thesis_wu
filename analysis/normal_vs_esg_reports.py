from pathlib import Path
import json
import numpy as np

report_stats_path = Path("reports") / "report_stats.json"

with open(report_stats_path, "r") as json_file:
    report_stats = json.load(json_file)

suffixes = ["ESG", "CSR", "SUS", "ENV", "NFI", "SR"] + ["INT"]

sentiment_differences = []
for company in report_stats.keys():
    reports = [r for r in report_stats[company].keys()]
    esg_reports = [r for r in reports if any([r.endswith(s) for s in suffixes])]
    reports = [r for r in reports if r not in esg_reports]

    if esg_reports:
        esg_sentiment_indexes = [
            (report_stats[company][r]["n_positive_words"] - report_stats[company][r]["n_negative_words"])
            / (report_stats[company][r]["n_positive_words"] + report_stats[company][r]["n_negative_words"])
            for r in esg_reports
        ]

        # alternative calc - taking all reports as one report -> one index
        n_esg_positives = sum([report_stats[company][r]["n_positive_words"] for r in esg_reports])
        n_esg_negatives = sum([report_stats[company][r]["n_negative_words"] for r in esg_reports])
        esg_sentiment_index_sum = (n_esg_positives - n_esg_negatives) / (n_esg_positives + n_esg_negatives)

        report_sentiment_indexes = [
            (report_stats[company][r]["n_positive_words"] - report_stats[company][r]["n_negative_words"])
            / (report_stats[company][r]["n_positive_words"] + report_stats[company][r]["n_negative_words"])
            for r in reports
        ]

        # alternative calc - taking all reports as one report -> one index
        n_rep_positives = sum([report_stats[company][r]["n_positive_words"] for r in reports])
        n_rep_negatives = sum([report_stats[company][r]["n_negative_words"] for r in reports])
        rep_sentiment_index_sum = (n_rep_positives - n_rep_negatives) / (n_rep_positives + n_rep_negatives)

        # print(np.mean(esg_sentiment_indexes), np.mean(report_sentiment_indexes))
        # print(esg_sentiment_index_sum, rep_sentiment_index_sum)

        sentiment_differences.append(np.mean(esg_sentiment_indexes) - np.mean(report_sentiment_indexes))

print("Average sentiment polarity difference of ESG minus non-ESG reports:")
print(np.mean(sentiment_differences))
