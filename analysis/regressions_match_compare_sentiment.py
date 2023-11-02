from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import json
from scipy import stats

with open(Path("results") / "match_compare_sentiments.json", "r") as json_file:
    results = json.load(json_file)
extras = pd.read_json(Path("common") / "company_extras.json", orient="index")
extras["esg"] = extras["esg"].replace("", np.nan).astype(float)

all_results = pd.DataFrame()

for company, company_dict in results.items():
    years = pd.DataFrame(company_dict).T.reset_index(names=["year"])
    years["company"] = company
    all_results = pd.concat([all_results, years])

all_results.reset_index(inplace=True, drop=True)
df = all_results.merge(extras, left_on="company", right_index=True)
# all_results["year"] = all_results["year"].astype(int)

y_2015 = df.loc[df["year"] == "2015", "pol_diff"].values
y_2016 = df.loc[df["year"] == "2016", "pol_diff"].values
y_2017 = df.loc[df["year"] == "2017", "pol_diff"].values
y_2018 = df.loc[df["year"] == "2018", "pol_diff"].values
y_2019 = df.loc[df["year"] == "2019", "pol_diff"].values
y_2020 = df.loc[df["year"] == "2020", "pol_diff"].values
y_2021 = df.loc[df["year"] == "2021", "pol_diff"].values
y_2022 = df.loc[df["year"] == "2022", "pol_diff"].values

H, pval = stats.kruskal(y_2015, y_2016, y_2017, y_2018, y_2019, y_2020, y_2021, y_2022)
# print(H, pval)

# sectors = df["sector"].unique().tolist()
# print(sectors)

consumer_defensive = df.loc[df["sector"] == "Consumer Defensive", "pol_diff"].values
consumer_cyclical = df.loc[df["sector"] == "Consumer Cyclical", "pol_diff"].values
technology = df.loc[df["sector"] == "Technology", "pol_diff"].values
basic_materials = df.loc[df["sector"] == "Basic Materials", "pol_diff"].values
industrials = df.loc[df["sector"] == "Industrials", "pol_diff"].values
financial_services = df.loc[df["sector"] == "Financial Services", "pol_diff"].values
healthcare = df.loc[df["sector"] == "Healthcare", "pol_diff"].values
communication_services = df.loc[df["sector"] == "Communication Services", "pol_diff"].values
utilities = df.loc[df["sector"] == "Utilities", "pol_diff"].values
energy = df.loc[df["sector"] == "Energy", "pol_diff"].values
real_estate = df.loc[df["sector"] == "Real Estate", "pol_diff"].values

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

model = smf.ols(formula="pol_diff ~ n_articles", data=df)
results = model.fit()
print(results.summary())

model = smf.ols(formula="pol_diff ~ n_articles", data=df)
results = model.fit()
print(results.summary())

print(df.columns)
