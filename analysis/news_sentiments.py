from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

news_results = pd.read_csv(Path("news") / "news_results.csv")

comp_years = (
    news_results.groupby(["company", "year"])[
        [
            "n_sentences",
            "n_esg_sentences",
            "n_positive_words",
            "n_negative_words",
            "n_positive_words_env",
            "n_negative_words_env",
            "n_positive_words_soc",
            "n_negative_words_soc",
            "n_positive_words_gov",
            "n_negative_words_gov",
        ]
    ]
    .sum()
    .reset_index()
)
comp_years["esg_ratio"] = comp_years["n_esg_sentences"] / comp_years["n_sentences"]


# def calc_sentiment_polarity(row):
#     return (row["n_positive_words"] - row["n_negative_words"]) / (row["n_positive_words"] + row["n_negative_words"])


def calc_sentiment_polarity(row, sub=None):
    subsub = f"_{sub}" if sub else ""
    if (row[f"n_negative_words{subsub}"] + row[f"n_positive_words{subsub}"]) == 0:
        return None
    return (row[f"n_positive_words{subsub}"] - row[f"n_negative_words{subsub}"]) / (
        row[f"n_positive_words{subsub}"] + row[f"n_negative_words{subsub}"]
    )


comp_years["sentiment_polarity"] = comp_years.apply(calc_sentiment_polarity, axis=1)
comp_years["sentiment_polarity_env"] = comp_years.apply(calc_sentiment_polarity, axis=1, sub="env")
comp_years["sentiment_polarity_soc"] = comp_years.apply(calc_sentiment_polarity, axis=1, sub="soc")
comp_years["sentiment_polarity_gov"] = comp_years.apply(calc_sentiment_polarity, axis=1, sub="gov")

# df_ = comp_years.groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
# fig = px.line(df_, x="year", y="sentiment", labels={"sentiment": "sentiment polarity"})
# fig.update_traces(line=dict(width=4))
# fig.update_layout(
#     title_text="Average sentiment polarity of reports by year",
#     title_x=0.5,
#     title_font=dict(size=20),
#     legend=dict(x=0.8, y=0.5, font=dict(size=20)),
#     xaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
#     yaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
# )
# fig.show()

fig = go.Figure()
df_ = comp_years.groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
fig.add_trace(go.Scatter(x=df_["year"], y=df_["sentiment"], mode="lines", name="Complete ESG", line=dict(width=4)))

df_ = comp_years.groupby("year")["sentiment_polarity_env"].mean().reset_index(name="sentiment")
fig.add_trace(go.Scatter(x=df_["year"], y=df_["sentiment"], mode="lines", name="Environmental", line=dict(width=4)))

df_ = comp_years.groupby("year")["sentiment_polarity_soc"].mean().reset_index(name="sentiment")
fig.add_trace(go.Scatter(x=df_["year"], y=df_["sentiment"], mode="lines", name="Social", line=dict(width=4)))

df_ = comp_years.groupby("year")["sentiment_polarity_gov"].mean().reset_index(name="sentiment")
fig.add_trace(go.Scatter(x=df_["year"], y=df_["sentiment"], mode="lines", name="Governance", line=dict(width=4)))

fig.update_layout(
    title_text="Average sentiment polarity of news articles by year (split by ESG sub-section)",
    title_x=0.5,
    title_y=0.95,
    title_font=dict(size=40),
    legend=dict(x=0.85, y=0, font=dict(size=30)),
    xaxis_title="Year",
    yaxis_title="Sentiment polarity",
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()
