"""
This script removes duplicates from the news articles.
"""

from pathlib import Path
import os
import time
import json
import regex

from utils import list_files, list_folders

t = time.time()

txt_folder = Path("news") / "txt"
news_stats = Path("news") / "news_stats.json"
tickers_path = Path("data_processing", "tickers.json")

with open(news_stats, "r") as json_file:
    news_stats = json.load(json_file)

companies = list_folders(txt_folder)
# companies = ["VOWG_p_DE"]
n_companies = len(companies)

for i, company in enumerate(companies):
    if not os.path.exists(txt_folder / company):
        os.mkdir(txt_folder / company)

    if company not in news_stats:
        news_stats[company] = {}

    news_files = list_files(txt_folder / company)
    # news_files = [news_files[0]]
    n_news_files = len(news_files)

    for j, news_file in enumerate(news_files):
        year, additional_info = regex.search(r"(\d{4})_?(\w+)?", news_file).groups()

        print(
            f'*** PROCESSING: {i+1}/{n_companies} {company}, {j+1}/{n_news_files} file from {year} {f"({additional_info}) " if additional_info else ""}***'
        )

        with open(txt_folder / company / news_file, "r") as text_file:
            articles = text_file.read().splitlines()

        titles = []
        remove_indexes = []

        for k, article in enumerate(articles):
            if not article:
                remove_indexes.append(k)
                continue
            article_words = article.split()
            ind = article_words.index("words") - 1
            if "Distributed" in article_words:
                ind_distributed = article_words.index("Distributed")
                ind = min(ind, ind_distributed)
            if ind:
                title = article_words[: ind - 1]
                title = " ".join(title)
                if title in titles:
                    remove_indexes.append(k)
                else:
                    titles.append(title)

        processed_articles = [a for l, a in enumerate(articles) if l not in remove_indexes]
        n_articles = len(processed_articles)
        processed_articles = "\n".join(processed_articles) + "\n"

        old_n_articles = news_stats[company][year]
        news_stats[company][year] = {"n_articles_old": old_n_articles, "n_articles_new": n_articles}

        with open(txt_folder / company / f"{company}_{year}.txt", "w") as text_file:
            text_file.write(processed_articles)

with open(Path("news") / "news_stats.json", "w") as json_file:
    json.dump(news_stats, json_file)

print(f"Time taken {((time.time() - t) / 60):.2f} minutes")
