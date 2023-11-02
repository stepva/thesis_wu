from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv(Path("reports") / "reports_results.csv")
suffixes = ["ESG", "CSR", "INT", "NFI", "ENV", "CSR_ENV", "CSR_2", "SUS", "SR"]
df["special"] = df["additional_info"].isin(suffixes)
df["esg_ratio"] = df["n_esg_sentences"] / df["n_sentences"]

extras = pd.read_json(Path("common") / "company_extras.json", orient="index")
extras["esg"] = extras["esg"].replace("", np.nan).astype(float)
df = df.merge(extras, left_on="company", right_index=True)

y_2015 = df.loc[df["year"] == 2015, "sentiment_polarity"].values
y_2016 = df.loc[df["year"] == 2016, "sentiment_polarity"].values
y_2017 = df.loc[df["year"] == 2017, "sentiment_polarity"].values
y_2018 = df.loc[df["year"] == 2018, "sentiment_polarity"].values
y_2019 = df.loc[df["year"] == 2019, "sentiment_polarity"].values
y_2020 = df.loc[df["year"] == 2020, "sentiment_polarity"].values
y_2021 = df.loc[df["year"] == 2021, "sentiment_polarity"].values
y_2022 = df.loc[df["year"] == 2022, "sentiment_polarity"].values

H, pval = stats.kruskal(y_2015, y_2016, y_2017, y_2018, y_2019, y_2020, y_2021, y_2022)
# print(H, pval)

consumer_defensive = df.loc[df["sector"] == "Consumer Defensive", "sentiment_polarity"].values
consumer_cyclical = df.loc[df["sector"] == "Consumer Cyclical", "sentiment_polarity"].values
technology = df.loc[df["sector"] == "Technology", "sentiment_polarity"].values
basic_materials = df.loc[df["sector"] == "Basic Materials", "sentiment_polarity"].values
industrials = df.loc[df["sector"] == "Industrials", "sentiment_polarity"].values
financial_services = df.loc[df["sector"] == "Financial Services", "sentiment_polarity"].values
healthcare = df.loc[df["sector"] == "Healthcare", "sentiment_polarity"].values
communication_services = df.loc[df["sector"] == "Communication Services", "sentiment_polarity"].values
utilities = df.loc[df["sector"] == "Utilities", "sentiment_polarity"].values
energy = df.loc[df["sector"] == "Energy", "sentiment_polarity"].values
real_estate = df.loc[df["sector"] == "Real Estate", "sentiment_polarity"].values

H, pval = stats.kruskal(
    consumer_defensive,
    consumer_cyclical,
    technology,
    basic_materials,
    industrials,
    financial_services,
    healthcare,
    communication_services,
    utilities,
    energy,
    real_estate,
)
# print(H, pval)

# print(df.groupby("sector")[["sentiment_polarity", "n_sentences"]].agg(["mean", "count"]))

df["esg_ratio_env"] = df["n_esg_sentences_env"] / df["n_sentences"]
df["esg_ratio_soc"] = df["n_esg_sentences_soc"] / df["n_sentences"]
df["esg_ratio_gov"] = df["n_esg_sentences_gov"] / df["n_sentences"]

model = smf.ols(formula="sentiment_polarity ~ esg_ratio + n_sentences", data=df)
results = model.fit()
print(results.summary())

model = smf.ols(formula="sentiment_polarity ~ esg_ratio_env + esg_ratio_soc + esg_ratio_gov + n_sentences", data=df)
results = model.fit()
print(results.summary())

model = smf.ols(formula="sentiment_polarity ~ esg + n_sentences + esg_ratio", data=df)
results = model.fit()
print(results.summary())

model = smf.ols(
    formula="sentiment_polarity ~ esg + n_sentences + esg_ratio_env + esg_ratio_soc + esg_ratio_gov", data=df
)
results = model.fit()
print(results.summary())

# print(df.columns)
