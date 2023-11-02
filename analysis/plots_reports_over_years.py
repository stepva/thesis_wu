from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

reports_results = pd.read_csv(Path("reports") / "reports_results.csv")

comp_years = (
    reports_results.groupby(["company", "year"])[
        ["n_pages", "n_sentences", "n_esg_sentences", "n_positive_words", "n_negative_words"]
    ]
    .sum()
    .reset_index()
)
comp_years["esg_ratio"] = comp_years["n_esg_sentences"] / comp_years["n_sentences"]

df_ = comp_years.groupby("year")["n_pages"].mean().reset_index(name="counts")
fig = px.line(df_, x="year", y="counts", labels={"counts": "Count", "year": "Year"})
fig.update_traces(line=dict(width=4))
fig.update_layout(
    title_text="Average number of report pages by year",
    title_x=0.5,
    title_y=0.98,
    title_font=dict(size=40),
    legend=dict(x=0.8, y=0.5, font=dict(size=30)),
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()

suffixes = ["ESG", "CSR", "INT", "NFI", "ENV", "CSR_ENV", "CSR_2", "SUS", "SR"]
special_reports = reports_results[reports_results["additional_info"].isin(suffixes)]
normal_reports = reports_results[~reports_results["additional_info"].isin(suffixes)]

# print(special_reports.shape[0] / reports_results.shape[0])

normal_reports = normal_reports.groupby(["company", "year"])[
    ["n_sentences", "n_esg_sentences", "n_positive_words", "n_negative_words"]
].sum()
normal_reports["esg_ratio"] = normal_reports["n_esg_sentences"] / normal_reports["n_sentences"]


special_reports = special_reports.groupby(["company", "year"])[
    ["n_sentences", "n_esg_sentences", "n_positive_words", "n_negative_words"]
].sum()
special_reports["esg_ratio"] = special_reports["n_esg_sentences"] / special_reports["n_sentences"]

fig = go.Figure()
df_ = comp_years.groupby("year")["esg_ratio"].mean().reset_index(name="ratio")
fig.add_trace(go.Scatter(x=df_["year"], y=df_["ratio"], mode="lines", name="All reports", line=dict(width=4)))

normals_ = normal_reports.groupby("year")["esg_ratio"].mean().reset_index(name="ratio")
fig.add_trace(
    go.Scatter(x=normals_["year"], y=normals_["ratio"], mode="lines", name="Normal reports", line=dict(width=4))
)

specials_ = special_reports.groupby("year")["esg_ratio"].mean().reset_index(name="ratio")
fig.add_trace(
    go.Scatter(x=specials_["year"], y=specials_["ratio"], mode="lines", name="Special reports", line=dict(width=4))
)

fig.update_layout(
    title_text="Average ratio of ESG-to-all sentences of reports by year (split by report type)",
    title_x=0.5,
    title_y=0.92,
    title_font=dict(size=20),
    legend=dict(x=0.8, y=0.5, font=dict(size=20)),
    xaxis_title="year",
    yaxis_title="ratio",
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
)
fig.show()


def calc_sentiment_polarity(row):
    return (row["n_positive_words"] - row["n_negative_words"]) / (row["n_positive_words"] + row["n_negative_words"])


comp_years["sentiment_polarity"] = comp_years.apply(calc_sentiment_polarity, axis=1)
df_ = comp_years.groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
fig = px.line(df_, x="year", y="sentiment", labels={"sentiment": "sentiment polarity"})
fig.update_traces(line=dict(width=4))
fig.update_layout(
    title_text="Average sentiment polarity of reports by year",
    title_x=0.5,
    title_font=dict(size=20),
    legend=dict(x=0.8, y=0.5, font=dict(size=20)),
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
)
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_["year"], y=df_["sentiment"], mode="lines", name="All reports", line=dict(width=4)))

special_reports["sentiment_polarity"] = special_reports.apply(calc_sentiment_polarity, axis=1)
specials_ = special_reports.groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
fig.add_trace(
    go.Scatter(x=specials_["year"], y=specials_["sentiment"], mode="lines", name="Special reports", line=dict(width=4))
)

normal_reports["sentiment_polarity"] = normal_reports.apply(calc_sentiment_polarity, axis=1)
normals_ = normal_reports.groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
fig.add_trace(
    go.Scatter(x=normals_["year"], y=normals_["sentiment"], mode="lines", name="Normal reports", line=dict(width=4))
)

fig.update_layout(
    title_text="Average sentiment polarity of reports by year (split by report type)",
    title_x=0.5,
    title_y=0.92,
    title_font=dict(size=20),
    legend=dict(x=0.8, y=0.5, font=dict(size=20)),
    xaxis_title="year",
    yaxis_title="sentiment polarity",
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
)
fig.show()

# # plt.title("Average sentiment polarity of reports per year\n(split by report type)")
# # plt.legend(["Special reports", "Normal reports"])
# # plt.savefig("results/reports_avg_sentiment_polarity_per_year_split.png")
# # if SHOW:
# #     plt.show()
# # else:
# #     plt.close()
