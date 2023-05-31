"""
This script prepares single files for positive, negative and uncertain words from the Loughran-McDonald dictionary.
"""

from pathlib import Path
import pandas as pd

sentiment_folder = Path('sentiment')
df = pd.read_csv(sentiment_folder / 'Loughran-McDonald_MasterDictionary_1993-2021.csv')

positive = df[df['Positive'] > 0]['Word'].str.lower().tolist()
with open(sentiment_folder / 'positive.txt', 'w') as file:
    file.write('\n'.join(positive))

negative = df[df['Negative'] > 0]['Word'].str.lower().tolist()
with open(sentiment_folder / 'negative.txt', 'w') as file:
    file.write('\n'.join(negative))

uncertainty = df[df['Uncertainty'] > 0]['Word'].str.lower().tolist()
with open(sentiment_folder / 'uncertain.txt', 'w') as file:
    file.write('\n'.join(uncertainty))

