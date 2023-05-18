"""
This script converts all pdf files of the company reports into plain txt files.
It also conducts some basic pre-processing, such as removing end of line hyphenation or extra spaces.
The resulting txt file should be readable but futher pre-processing before any NLP is needed.
The idea of pages is not preserved, so the text is just one long line string.
Note that there are still some issues, such as occassional spaces in the middle of words, due to the PyPDF2 package.
"""

import PyPDF2
import regex
from pathlib import Path
import os
import time
import json

from utils import list_folders, list_files

t = time.time()

pdf_folder = Path('reports') / 'pdf'
txt_folder = Path('reports') / 'txt'
report_stats_path = Path('reports') / "report_stats.json"

if os.path.exists(report_stats_path):
    with open(report_stats_path, "r") as json_file:
        report_stats = json.load(json_file)
else:
    report_stats = {}

companies = list_folders(pdf_folder)
# companies = [companies[0]]
n_companies = len(companies)

for i, company in enumerate(companies):
    if not os.path.exists(txt_folder / company):
        os.mkdir(txt_folder / company)

    if company not in report_stats:
        report_stats[company] = {}

    pdf_reports = list_files(pdf_folder / company)
    # pdf_reports = [pdf_reports[3]]
    n_reports = len(pdf_reports)

    try:
        for j, report in enumerate(pdf_reports):
            year, additional_info = regex.search(r'(\d{4})_?(\w+)?', report).groups()
            report_name = report.replace('.pdf', '')

            print(f'*** PROCESSING: {i+1}/{n_companies} {company}, {j+1}/{n_reports} report from {year} {f"({additional_info}) " if additional_info else ""}***')

            if os.path.exists(txt_folder / company / report.replace('pdf', 'txt')):
                print('\t Skipped, already processed earlier')
                continue

            report_stats[company][report_name] = {}

            with open(pdf_folder / company / report, 'rb') as file:
                t_report = time.time()
                reader = PyPDF2.PdfReader(file)
                pages = reader.pages
                n_pages = len(pages)

                print(f"\t {n_pages} pages")
                
                text = ""
                for page in pages:
                    page_text = page.extract_text()

                    # remove spaces before punctuation
                    page_text = regex.sub(r'(\s+)([.,?!])', '\g<2>', page_text)
                    # remove end of line hyphenation
                    page_text = regex.sub(r'\s*-\n', '', page_text)
                    # remove extra spaces
                    page_text = regex.sub(r'\s+', ' ', page_text)

                    text += page_text
                

                time_taken = time.time() - t_report
                print(f"\t Time taken - {time_taken:.2f} seconds")

                report_stats[company][report_name] = {'time_taken': time_taken, 'n_pages': n_pages}


            with open(txt_folder / company / report.replace('pdf', 'txt'), "w") as text_file:
                text_file.write(text)
    except Exception as e:
        print(f'ERROR: {e}')
        break

with open(Path('reports') / "report_stats.json", "w") as json_file:
    json.dump(report_stats, json_file)

print(f"Time taken {((time.time() - t) / 60):.2f} minutes")