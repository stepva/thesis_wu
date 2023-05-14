"""
This script converts rtf files with relevant news articles downloaded from Factiva to txt.
The resulting txt file should be readable, it contains one article per line.
Futher pre-processing before any NLP is needed.
"""

from pathlib import Path
import os
import time
import json
import regex

import pypandoc

from utils import list_files

t = time.time()

news_folder = Path('news') / 'original'
txt_folder = Path('news') / 'txt'
news_stats = Path('news') / "news_stats.json"
tickers_path = Path('tickers.json')

if os.path.exists(news_stats):
    with open(news_stats, "r") as json_file:
        news_stats = json.load(json_file)
else:
    news_stats = {}

with open(tickers_path, "r") as json_file:
    tickers = json.load(json_file)

n_companies = len(tickers.keys())

# tickers = {'ABI_BR': 'ABI'}
for i, (company, news_ticker) in enumerate(tickers.items()):
    if not os.path.exists(txt_folder / company):
        os.mkdir(txt_folder / company)

    if company not in news_stats:
        news_stats[company] = {}

    news_files = list_files(news_folder / news_ticker)
    # news = ['ABI_2021.rtf', 'ABI_2021_2.rtf']
    n_news_files = len(news_files)

    try:
        for j, news_file in enumerate(news_files):
            year, additional_info = regex.search(r'(\d{4})_?(\w+)?', news_file).groups()

            print(f'*** PROCESSING: {i+1}/{n_companies} {company}, {j+1}/{n_news_files} file from {year} {f"({additional_info}) " if additional_info else ""}***')

            articles = pypandoc.convert_file(news_folder / news_ticker / news_file, 'plain', format='rtf')
            articles = regex.split(r'Document \S{25}', articles)[:-1]

            processed_articles = []
            for article in articles: 
                    # remove extra spaces
                    article = regex.sub(r'\s+', ' ', article)
                    if article[0] == ' ':
                        article = article[1:]
                    processed_articles.append(article)

            n_articles = len(processed_articles)
            print(f"\t {n_articles} articles")
            processed_articles = '\n'.join(processed_articles) + '\n'

            if year in news_stats[company]:
                news_stats[company][year] += n_articles
            else:
                news_stats[company][year] = n_articles

            with open(txt_folder / company / f'{company}_{year}.txt', "a") as text_file:
                text_file.write(processed_articles)
    
    except Exception as e:
        print(f'ERROR: {e}')
        break

with open(Path('news') / "news_stats.json", "w") as json_file:
    json.dump(news_stats, json_file)

print(f"Time taken {((time.time() - t) / 60):.2f} minutes")