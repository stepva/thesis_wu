"""
This script prepares the txt news articles for sentiment analysis.
It follows a similar procedure as the reports_sentiment_pre_process.py script.
On top of that, it also saves the date of the article at the beginning, for further precision date matching.
"""

from pathlib import Path
import time
import nltk
import regex
import os
from datetime import datetime

from data_processing.utils import list_folders, list_files

t = time.time()

txt_folder = Path("news") / "txt"
sentiment_ready = Path("news") / "sentiment_ready"

companies = list_folders(txt_folder)
# companies = [companies[0]]
n_company = len(companies)

for i, company in enumerate(companies):
    if not os.path.exists(sentiment_ready / company):
        os.mkdir(sentiment_ready / company)

    news_files = list_files(txt_folder / company)
    # news_files = [news_files[0]]
    n_news_files = len(news_files)

    for j, news_file in enumerate(news_files):
        year, additional_info = regex.search(r"(\d{4})_?(\w+)?", news_file).groups()

        print(
            f'*** PRE-PROCESSING: {i+1}/{n_company} {company}, {j+1}/{n_news_files} file from {year} {f"({additional_info}) " if additional_info else ""}***'
        )

        with open(txt_folder / company / news_file, "r") as text_file:
            articles = text_file.read().splitlines()

        processed_articles = []
        for article in articles:
            date = regex.search(r" (\d{1,2} [A-Z][a-z]{3,} \d{4}|\d+ May \d{4})", article).groups()[0]
            date = datetime.strptime(date, "%d %B %Y").date().strftime("%Y-%m-%d")

            article = article.lower()
            article = regex.sub(r"[^a-z\s]", "", article)
            article = regex.sub(r"\s+", " ", article)
            article = regex.sub(r"^\s", "", article)

            stop_words = nltk.corpus.stopwords.words("english")
            # against is a stop word, but we want to keep it, since it is also a negative word
            stop_words.remove("against")

            # remove stop words
            article = [w for w in article.split() if w not in stop_words]

            # remove words with less than 3 characters
            article = [w for w in article if len(w) > 2]

            processed_articles.append(" ".join([date] + article))

        processed_articles = "\n".join(processed_articles) + "\n"

        with open(sentiment_ready / company / f"{company}_{year}.txt", "w") as text_file:
            text_file.write(processed_articles)

print(f"Time taken: {time.time() - t:.2f} seconds")
