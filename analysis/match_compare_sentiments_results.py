from pathlib import Path
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

with open(Path("results") / "match_compare_sentiments.json", "r") as json_file:
    results = json.load(json_file)
extras = pd.read_json(Path("common") / "company_extras.json", orient="index").reset_index(names=["company"])
extras = extras.merge(extras.groupby("sector")["company"].nunique().reset_index(name="sector_n"), on="sector")
extras["sector_with_n"] = extras["sector"] + " (" + extras["sector_n"].astype(str) + ")"

# print("Number of report years:")
# n_report_years = 0
# for company, comp_dict in results.items():
#     n_report_years += len(comp_dict)
# print(n_report_years)

# print("Number of companies:")
# print(len(results))

# print("Number of news articles:")
# n_articles = 0
# for company, comp_dict in results.items():
#     for year, year_dict in comp_dict.items():
#         n_articles += year_dict["n_articles"]
# print(n_articles)

articles_per_report_year = {}
for year in range(2015, 2023):
    year = str(year)
    articles_per_report_year[year] = []
    for c in results.keys():
        if year in results[c].keys():
            articles_per_report_year[year].append(results[c][year]["n_articles"])

means = {y: np.mean(articles_per_report_year[y]) for y in articles_per_report_year.keys()}

fig = go.Figure()
fig.add_trace(
    go.Scatter(x=list(means.keys()), y=list(means.values()), mode="lines", name="All companies", line=dict(width=4))
)

cc = extras[extras["sector"] == "Consumer Cyclical"]["company"].unique().tolist()
cc_means = {}
for year in range(2015, 2023):
    year = str(year)
    cc_means[year] = []
    for c in [rk for rk in results.keys() if rk in cc]:
        if year in results[c].keys():
            cc_means[year].append(results[c][year]["n_articles"])
cc_means = {y: np.mean(cc_means[y]) for y in cc_means.keys()}

fig.add_trace(
    go.Scatter(
        x=list(cc_means.keys()), y=list(cc_means.values()), mode="lines", name="Consumer Cyclical", line=dict(width=4)
    )
)

ind = extras[extras["sector"] == "Industrials"]["company"].unique().tolist()
ind_means = {}
for year in range(2015, 2023):
    year = str(year)
    ind_means[year] = []
    for c in [rk for rk in results.keys() if rk in ind]:
        if year in results[c].keys():
            ind_means[year].append(results[c][year]["n_articles"])
ind_means = {y: np.mean(ind_means[y]) for y in ind_means.keys()}

fig.add_trace(
    go.Scatter(
        x=list(ind_means.keys()), y=list(ind_means.values()), mode="lines", name="Industrials", line=dict(width=4)
    )
)

fin = extras[extras["sector"] == "Financial Services"]["company"].unique().tolist()
fin_means = {}
for year in range(2015, 2023):
    year = str(year)
    fin_means[year] = []
    for c in [rk for rk in results.keys() if rk in fin]:
        if year in results[c].keys():
            fin_means[year].append(results[c][year]["n_articles"])
fin_means = {y: np.mean(fin_means[y]) for y in fin_means.keys()}

fig.add_trace(
    go.Scatter(
        x=list(fin_means.keys()),
        y=list(fin_means.values()),
        mode="lines",
        name="Financial Services",
        line=dict(width=4),
    )
)

fig.update_layout(
    title_text="Average number of news articles per report year (selected sectors)",
    title_x=0.5,
    title_y=0.95,
    title_font=dict(size=40),
    legend=dict(x=0, y=1, font=dict(size=30)),
    xaxis_title="Year",
    yaxis_title="Count",
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()

pol_diffs = []
for company, comp_dict in results.items():
    for year, year_dict in comp_dict.items():
        pol_diffs.append(year_dict["pol_diff"])
print("Mean difference in polarity:")
print(np.median(pol_diffs))

pol_diffs_year = {}
for year in range(2015, 2023):
    year = str(year)
    pol_diffs_year[year] = []
    for c in results.keys():
        if year in results[c].keys():
            pol_diffs_year[year].append(results[c][year]["pol_diff"])
pol_diffs_year = {y: np.mean(pol_diffs_year[y]) for y in pol_diffs_year.keys()}

pol_diffs_year_env = {}
for year in range(2015, 2023):
    year = str(year)
    pol_diffs_year_env[year] = []
    for c in results.keys():
        if year in results[c].keys():
            if "pol_diff_env" not in results[c][year]:
                continue
            pol_diffs_year_env[year].append(results[c][year]["pol_diff_env"])
pol_diffs_year_env = {y: np.mean(pol_diffs_year_env[y]) for y in pol_diffs_year_env.keys()}

pol_diffs_year_soc = {}
for year in range(2015, 2023):
    year = str(year)
    pol_diffs_year_soc[year] = []
    for c in results.keys():
        if year in results[c].keys():
            if "pol_diff_soc" not in results[c][year]:
                continue
            pol_diffs_year_soc[year].append(results[c][year]["pol_diff_soc"])
pol_diffs_year_soc = {y: np.mean(pol_diffs_year_soc[y]) for y in pol_diffs_year_soc.keys()}

pol_diffs_year_gov = {}
for year in range(2015, 2023):
    year = str(year)
    pol_diffs_year_gov[year] = []
    for c in results.keys():
        if year in results[c].keys():
            if "pol_diff_gov" not in results[c][year]:
                continue
            pol_diffs_year_gov[year].append(results[c][year]["pol_diff_gov"])
pol_diffs_year_gov = {y: np.mean(pol_diffs_year_gov[y]) for y in pol_diffs_year_gov.keys()}

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=list(pol_diffs_year.keys()),
        y=list(pol_diffs_year.values()),
        mode="lines",
        name="Complete ESG",
        line=dict(width=4),
    )
)

fig.add_trace(
    go.Scatter(
        x=list(pol_diffs_year_env.keys()),
        y=list(pol_diffs_year_env.values()),
        mode="lines",
        name="Environmental",
        line=dict(width=4),
    )
)

fig.add_trace(
    go.Scatter(
        x=list(pol_diffs_year_soc.keys()),
        y=list(pol_diffs_year_soc.values()),
        mode="lines",
        name="Social",
        line=dict(width=4),
    )
)
fig.add_trace(
    go.Scatter(
        x=list(pol_diffs_year_gov.keys()),
        y=list(pol_diffs_year_gov.values()),
        mode="lines",
        name="Governance",
        line=dict(width=4),
    )
)
fig.update_traces(line=dict(width=4))
fig.update_layout(
    title_text="Average difference in polarity between reports and news articles (split by ESG sub-section)",
    title_x=0.5,
    title_y=0.95,
    title_font=dict(size=40),
    xaxis_title="Year",
    yaxis_title="Polarity difference",
    legend=dict(x=0, y=1, font=dict(size=30)),
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()

sectors = list(extras["sector_with_n"].unique())
pol_diffs_year_sectors = {}
for sector in sectors:
    pol_diffs_year_sectors[sector] = {}
    for year in range(2015, 2023):
        year = str(year)
        pol_diffs_year_sectors[sector][year] = []
        for c in extras[extras["sector_with_n"] == sector]["company"].unique().tolist():
            if year in results[c].keys():
                pol_diffs_year_sectors[sector][year].append(results[c][year]["pol_diff"])
    pol_diffs_year_sectors[sector] = {
        y: np.mean(pol_diffs_year_sectors[sector][y]) for y in pol_diffs_year_sectors[sector].keys()
    }

pol_diffs_year_sectors = pd.DataFrame(pol_diffs_year_sectors).T
fig = px.bar(pol_diffs_year_sectors, barmode="group")
fig.update_layout(
    title_text="Average difference in polarity between reports and news articles accross sectors and years",
    title_x=0.5,
    title_font=dict(size=40),
    legend=dict(x=0, y=1, font=dict(size=10), title=""),
    xaxis_title="Sector",
    yaxis_title="Polarity difference",
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=12)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()
