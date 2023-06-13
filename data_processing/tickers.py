"""
This prepares a json file with the mapping between the company tickers and the news tickers.
(I used different tickers for the news and the reports, either RIC or "standard" ticker)
"""

import pandas as pd
import json

df = pd.read_excel("data_processing/reports_overview.xlsx")

df["Ticker/RIC"] = df["Ticker/RIC"].str.replace(".", "_")
tickers = df[["Ticker/RIC", "News Ticker"]].to_dict(orient="records")
tickers = {t["Ticker/RIC"]: t["News Ticker"] for t in tickers}

with open("data_processing/tickers.json", "w") as file:
    json.dump(tickers, file)
