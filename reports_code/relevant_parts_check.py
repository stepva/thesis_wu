"""
This script provides some basic and descriptive statistics on the processed relevant ESG sentences.
It checks the ration of ESG to all sentences for each report to spot out obvious issues.
It also checks the lengths of the sentences, noting that further processing is needed before the sentiment analysis.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import json

esg_folder = Path('reports') / 'esg_relevant'
report_stats_path = Path('reports') / "report_stats.json"

with open(report_stats_path, "r") as json_file:
    report_stats = json.load(json_file)

# check if lenghts make sense - suggests all reports were processed correctly
all_sentences = np.array([c[r]['n_sentences'] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(all_sentences, columns=['lengths']).describe())

esg_sentences = np.array([c[r]['n_esg_sentences'] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(esg_sentences, columns=['times']).describe())

ratio = np.array([c[r]['n_esg_sentences'] / c[r]['n_sentences'] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(ratio, columns=['pages']).describe())

# reports with highest ratio of ESG sentences are mostly _ESG or similar reports, which is good
ratio_with_names = [(c[r]['n_esg_sentences'] / c[r]['n_sentences'], r) for c in report_stats.values() for r in c.keys()]
ratio_with_names.sort(key=lambda x: x[0], reverse=True)
print(ratio_with_names[:10])

# special report suffixes
suffixes = ['ESG', 'CSR', 'SUS', 'SR', 'NFI', 'ENV', 'INT']

# average ratio of ESG sentences in normal reports is lower than in special reports, good
normal_reports = [(r, n) for r, n in ratio_with_names if not any(f'_{s}' in n for s in suffixes)]
normal_reports_ratio = [r for r, n in normal_reports]
print(np.mean(normal_reports_ratio), len(normal_reports_ratio))

special_reports = [(r, n) for r, n in ratio_with_names if any(f'_{s}' in n for s in suffixes)]
special_reports_ratio = [r for r, n in special_reports]
print(np.mean(special_reports_ratio), len(special_reports_ratio))

min_lengths = []
avg_lengths = []
max_lengths = []
all_lengths = []
for company in report_stats.keys():
    for report in report_stats[company].keys():
        esg_txt = esg_folder / company / f'{report}.txt'
        with open(esg_txt, 'r') as file:
            sentences = file.readlines()
            sentences = [s.rstrip().split() for s in sentences]
            lengths = [len(s) for s in sentences]
            min_lengths.append(min(lengths))
            avg_lengths.append(np.mean(lengths))
            max_lengths.append(max(lengths))
            all_lengths += lengths

print(pd.DataFrame(np.array(min_lengths), columns=['min']).describe())
print(pd.DataFrame(np.array(avg_lengths), columns=['avg']).describe())
print(pd.DataFrame(np.array(max_lengths), columns=['max']).describe())
print(pd.DataFrame(np.array(all_lengths), columns=['all']).describe())

# I will have to filter the sentences based on length after processing them further before the sentiment
# clearly, there are some too short ones and some too long ones, because of how the pdfs were processed
# the average looks good though