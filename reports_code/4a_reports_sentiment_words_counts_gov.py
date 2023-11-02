"""
This script counts occurences of positive and negative words in the processed relevant ESG sentences.
Sentences longer than 100 words are removed - this can be played with, see comments in sentiment_processing_check.py.
The results are saved in the report_stats.json file.
The actual words and their counts are also saved, in the report_sentiment_words.json file.
"""

from pathlib import Path
import time
from collections import Counter
import regex
import os
import json

from common.utils import list_folders, list_files

t = time.time()

sentiment_ready = Path("reports") / "sentiment_ready_gov"
report_stats_path = Path("reports") / "report_stats.json"

if os.path.exists(report_stats_path):
    with open(report_stats_path, "r") as json_file:
        report_stats = json.load(json_file)

with open("sentiment/positive.txt", "r") as file:
    positive = file.read().splitlines()

with open("sentiment/negative.txt", "r") as file:
    negative = file.read().splitlines()

report_sentiment_words = {}

companies = list_folders(sentiment_ready)
# companies = [companies[0]]
n_company = len(companies)

for i, company in enumerate(companies):
    if not os.path.exists(sentiment_ready / company):
        os.mkdir(sentiment_ready / company)

    reports = list_files(sentiment_ready / company)
    # reports = [reports[0]]
    n_reports = len(reports)

    if company not in report_sentiment_words:
        report_sentiment_words[company] = {}

    for j, report in enumerate(reports):
        year, additional_info = regex.search(r"(\d{4})_?(\w+)?", report).groups()
        report_name = report.replace(".txt", "")

        print(
            f'*** SENTIMENTING: {i+1}/{n_company} {company}, {j+1}/{n_reports} report from {year} {f"({additional_info}) " if additional_info else ""}***'
        )

        with open(sentiment_ready / company / report, "r") as text_file:
            sentences = text_file.read().splitlines()

        # remove sentences longer than 100 words
        sentences = [s for s in sentences if len(s.split()) <= 100]

        all_words = [word for s in sentences for word in s.split()]

        all_words_counter = Counter(all_words)
        positive_words = {word: all_words_counter[word] for word in positive}
        positive_words = {k: v for k, v in positive_words.items() if v > 0}

        negative_words = {word: all_words_counter[word] for word in negative}
        negative_words = {k: v for k, v in negative_words.items() if v > 0}

        positive_count = sum(positive_words.values())
        negative_count = sum(negative_words.values())

        report_stats[company][report_name]["n_positive_words_gov"] = positive_count
        report_stats[company][report_name]["n_negative_words_gov"] = negative_count

        report_sentiment_words[company][report_name] = {
            "positive_words": positive_words,
            "negative_words": negative_words,
        }

with open(Path("reports") / "report_stats.json", "w") as json_file:
    json.dump(report_stats, json_file)

with open(Path("reports") / "report_sentiment_words_gov.json", "w") as json_file:
    json.dump(report_sentiment_words, json_file)

print(f"Time taken: {time.time() - t:.2f} seconds")
