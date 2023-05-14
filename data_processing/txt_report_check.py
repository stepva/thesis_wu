"""
This script provides some basic and descriptive statistics on the processed reports.
This allows to check if all reports were processed correctly.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import json

CALC_LEN = False

txt_folder = Path('reports') / 'txt'
report_stats_path = Path('reports') / "report_stats.json"

with open(report_stats_path, "r") as json_file:
    report_stats = json.load(json_file)

if CALC_LEN:
    for company in report_stats.keys():
        for report in report_stats[company].keys():
            report_txt = txt_folder / company / f'{report}.txt'
            with open(report_txt, 'r') as file:
                text = file.read()
                report_stats[company][report]['length'] = len(text)

# check if lenghts make sense - suggests all reports were processed correctly
lengths = np.array([c[r]['length'] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(lengths, columns=['lengths']).describe())

times = np.array([c[r]['time_taken'] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(times, columns=['times']).describe())

pages = np.array([c[r]['n_pages'] for c in report_stats.values() for r in c.keys()])
print(pd.DataFrame(pages, columns=['pages']).describe())

with open(Path('reports') / "report_stats.json", "w") as json_file:
    json.dump(report_stats, json_file)

