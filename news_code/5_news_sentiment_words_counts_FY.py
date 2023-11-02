"""
This script counts occurences of positive and negative words in the news articles.
The results are saved in the news_stats.json file.
The actual words and their counts are also saved, in the news_sentiment_words.json file.
"""

from pathlib import Path
import time
import regex
import os
import json
from collections import Counter
from datetime import datetime

from common.utils import list_files

t = time.time()

news_folder = Path("news")
sentiment_ready = news_folder / "sentiment_ready"
news_stats_path = news_folder / "news_stats.json"

if os.path.exists(news_stats_path):
    with open(news_stats_path, "r") as json_file:
        news_stats = json.load(json_file)

with open("sentiment/positive.txt", "r") as file:
    positive = file.read().splitlines()

with open("sentiment/negative.txt", "r") as file:
    negative = file.read().splitlines()

with open(Path("common") / "company_extras.json", "r") as json_file:
    extras = json.load(json_file)

with open(Path("news") / "news_sentiment_words.json", "r") as json_file:
    news_sentiment_words = json.load(json_file)

companies = [c for c in extras if "fiscal_year" in extras[c].keys()]
# companies = [companies[0]]
n_company = len(companies)

for i, company in enumerate(companies):
    news_files = list_files(sentiment_ready / company)
    # news_files = [news_files[0]]
    n_news_files = len(news_files)

    if company not in news_sentiment_words:
        news_sentiment_words[company] = {}

    all_articles = []
    years = []

    for j, news_file in enumerate(news_files):
        year, additional_info = regex.search(r"(\d{4})_?(\w+)?", news_file).groups()

        with open(sentiment_ready / company / news_file, "r") as text_file:
            articles = text_file.read().splitlines()

        all_articles.extend(articles)
        years.append(int(year))

    fy = extras[company]["fiscal_year"]

    for year in years:
        y = 1
        if company in ["ITX_MC", "PERP_PA"]:
            y = 0
        fy_dates = [f"{year-y}-{fy[0]}-01", f"{year-y+1}-{fy[1]}-01"]
        fy_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in fy_dates]

        print(f"*** SENTIMENTING: {i+1}/{n_company} {company}, fiscal year {year} ({fy_dates[0]} - {fy_dates[1]})***")

        articles = [
            a
            for a in all_articles
            if fy_dates[0] <= datetime.strptime(a.split(" ")[0], "%Y-%m-%d").date() < fy_dates[1]
        ]
        n_articles = len(articles)

        all_words = [word for a in articles for word in a.split()]

        all_words_counter = Counter(all_words)
        positive_words = {word: all_words_counter[word] for word in positive}
        positive_words = {k: v for k, v in positive_words.items() if v > 0}

        negative_words = {word: all_words_counter[word] for word in negative}
        negative_words = {k: v for k, v in negative_words.items() if v > 0}

        positive_count = sum(positive_words.values())
        negative_count = sum(negative_words.values())

        year = str(year)
        if year not in news_stats[company].keys():
            news_stats[company][year] = {}

        news_stats[company][year]["n_articles_processed_fy"] = n_articles
        news_stats[company][year]["n_positive_words_fy"] = positive_count
        news_stats[company][year]["n_negative_words_fy"] = negative_count

    news_sentiment_words[company][year] = {"positive_words_fy": positive_words, "negative_words_fy": negative_words}


with open(news_folder / "news_stats.json", "w") as json_file:
    json.dump(news_stats, json_file)

with open(news_folder / "news_sentiment_words.json", "w") as json_file:
    json.dump(news_sentiment_words, json_file)

print(f"Time taken: {time.time() - t:.2f} seconds")
