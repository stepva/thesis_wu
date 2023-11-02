"""
This script extracts the relevant parts of the news articles, i.e. the sentences that contain ESG words.
It also prepares the sentences for sentiment analysis, i.e. removes stop words, removes words with less than 3 characters, etc.
Furthermore it also extracts the date of the article and adds it to its beginning.
"""

from pathlib import Path
import time
import nltk
import regex
import json
import os
from datetime import datetime

from common.utils import list_folders, list_files

t = time.time()

# load ESG word list
# there are 2 words with 2 words in the list (climate change, global warming)
# both "climate" and "warming" are included independentyl as well, so can ignore these
with open(Path("esg_words", "baier_soc.txt"), "r") as text_file:
    esg_words = text_file.readlines()
    esg_words = [w.rstrip().lower() for w in esg_words]

txt_folder = Path("news") / "txt"
sentiment_ready = Path("news") / "sentiment_ready_soc"
news_stats = Path("news") / "news_stats.json"

with open(news_stats, "r") as json_file:
    news_stats = json.load(json_file)

companies = list_folders(txt_folder)
# companies = ["TTEF_PA"]
n_company = len(companies)

if not os.path.exists(sentiment_ready):
    os.mkdir(sentiment_ready)

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
        n_esg_sentences_total = 0
        for article in articles:
            if len(article.split()) < 5:
                continue
            date = regex.search(r" (\d{1,2} [A-Z][a-z]{3,} \d{4}|\d+ May \d{4})", article).groups()[0]
            date = datetime.strptime(date, "%d %B %Y").date().strftime("%Y-%m-%d")

            # tokenize into sentences
            sentences = nltk.tokenize.sent_tokenize(article)
            sentences = [s.lower() for s in sentences]

            # tokenize sentences into words (numbers and weird signs still included)
            sentences = [nltk.tokenize.word_tokenize(s) for s in sentences]
            n_sentences = len(sentences)

            # indexes of sentences with ESG words
            esg_sentences_id = set([i for i, s in enumerate(sentences) if any(w in s for w in esg_words)])
            n_esg_sentences = len(esg_sentences_id)
            n_esg_sentences_total += n_esg_sentences

            # actual sentences with ESG words
            esg_sentences = [sentences[i] for i in esg_sentences_id]
            esg_sentences = [" ".join(s) for s in esg_sentences]

            article = " ".join(esg_sentences)

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

        # news_stats[company][year]["n_articles_processed"] = len(processed_articles)
        # news_stats[company][year]["n_sentences"] = n_sentences
        news_stats[company][year]["n_esg_sentences_soc"] = n_esg_sentences_total
        processed_articles = "\n".join(processed_articles) + "\n"

        with open(sentiment_ready / company / f"{company}_{year}.txt", "w") as text_file:
            text_file.write(processed_articles)

with open(Path("news") / "news_stats.json", "w") as json_file:
    json.dump(news_stats, json_file)

print(f"Time taken: {time.time() - t:.2f} seconds")
