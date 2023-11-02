"""
This script uses the "baier.txt" (BaierBerningerKiesel ESG, vJuly 2022) word list to extract the relevant parts of the reports.
It does some further minor processing and fixing of the txt processed reports and then tokenizes the text to sentences and further to words.
It still keeps all numbers, weird stuff and all forms of words, because the word list includes all forms of relevant words.
It looks for sentences which contain any of the words from the word list and keeps only those sentences, saved in a new txt file for each report.
"""

from pathlib import Path
import time
import nltk
import regex
import os
import json

from common.utils import list_folders, list_files

t = time.time()

# load ESG word list
# there are 2 words with 2 words in the list (climate change, global warming)
# both "climate" and "warming" are included independentyl as well, so can ignore these
with open(Path("esg_words", "baier_gov.txt"), "r") as text_file:
    esg_words = text_file.readlines()
    esg_words = [w.rstrip().lower() for w in esg_words]

esg_folder = Path("reports") / "esg_relevant_gov"
txt_folder = Path("reports") / "txt"
report_stats_path = Path("reports") / "report_stats.json"

if os.path.exists(report_stats_path):
    with open(report_stats_path, "r") as json_file:
        report_stats = json.load(json_file)

companies = list_folders(txt_folder)
# companies = [companies[0]]
n_companies = len(companies)

if not os.path.exists(esg_folder):
    os.mkdir(esg_folder)

for i, company in enumerate(companies):
    if not os.path.exists(esg_folder / company):
        os.mkdir(esg_folder / company)

    reports = list_files(txt_folder / company)
    # report = reports[-1]
    n_reports = len(reports)

    for j, report in enumerate(reports):
        year, additional_info = regex.search(r"(\d{4})_?(\w+)?", report).groups()
        report_name = report.replace(".txt", "")

        print(
            f'*** PROCESSING: {i+1}/{n_companies} {company}, {j+1}/{n_reports} report from {year} {f"({additional_info}) " if additional_info else ""}***'
        )

        with open(txt_folder / company / report, "r") as text_file:
            text = text_file.read()

        # remove '-'s inside words (issue from pdf reading)
        text = regex.sub(r"(\S)(-)(\S)", "\g<1>\g<3>", text)

        # tokenize into sentences
        sentences = nltk.tokenize.sent_tokenize(text)
        sentences = [s.lower() for s in sentences]

        # tokenize sentences into words (numbers and weird signs still included)
        sentences = [nltk.tokenize.word_tokenize(s) for s in sentences]

        n_sentences = len(sentences)

        # indexes of sentences with ESG words
        esg_sentences_id = set([i for i, s in enumerate(sentences) if any(w in s for w in esg_words)])
        n_esg_sentences = len(esg_sentences_id)

        # actual sentences with ESG words
        esg_sentences = [sentences[i] for i in esg_sentences_id]
        esg_sentences = [" ".join(s) for s in esg_sentences]

        with open(esg_folder / company / report, "w") as text_file:
            text_file.write("\n".join(esg_sentences))

        # report_stats[company][report_name]["n_sentences"] = n_sentences
        report_stats[company][report_name]["n_esg_sentences_gov"] = n_esg_sentences

with open(Path("reports") / "report_stats.json", "w") as json_file:
    json.dump(report_stats, json_file)

print(f"Time taken {((time.time() - t) / 60):.2f} minutes")
