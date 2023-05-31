"""
This script takes files with ESG relevant sentences and prepares them for sentiment analysis.
It removes punctuation, stop words (except "against") and words with less than 3 characters.
The result is saved in new txt files per report.
"""

from pathlib import Path
import time
import nltk
import regex
import os

from data_processing.utils import list_folders, list_files

t = time.time()

esg_folder = Path('reports') / 'esg_relevant'
sentiment_ready = Path('reports') / 'sentiment_ready'

companies = list_folders(esg_folder)
# company = companies[0]
n_company = len(companies)

for i, company in enumerate(companies):
    if not os.path.exists(sentiment_ready / company):
        os.mkdir(sentiment_ready / company)

    reports = list_files(esg_folder / company)
    report = reports[-1]
    n_reports = len(reports)
    
    for j, report in enumerate(reports):
        year, additional_info = regex.search(r'(\d{4})_?(\w+)?', report).groups()
        report_name = report.replace('.txt', '')

        print(f'*** PROCESSING: {i+1}/{n_company} {company}, {j+1}/{n_reports} report from {year} {f"({additional_info}) " if additional_info else ""}***')

        with open(esg_folder / company / report, "r") as text_file:
            sentences = text_file.read().splitlines()

        sentences = [regex.sub(r'[^a-z\s]', '', s) for s in sentences]
        sentences = [regex.sub(r'\s+', ' ', s) for s in sentences]
        sentences = [regex.sub(r'^\s', '', s) for s in sentences]

        stop_words = nltk.corpus.stopwords.words('english')
        # against is a stop word, but we want to keep it, since it is also a negative word
        stop_words.remove('against')

        # remove stop words
        sentences = [[w for w in s.split() if w not in stop_words] for s in sentences]

        # remove words with less than 3 characters
        sentences = [[w for w in s if len(w) > 2] for s in sentences]

        sentences = [' '.join(s) for s in sentences]

        with open(sentiment_ready / company / report, "w") as text_file:
            text_file.write('\n'.join(sentences))

print(f'Time taken: {time.time() - t:.2f} seconds')