from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv(Path("news") / "news_results.csv")
extras = pd.read_json(Path("common") / "company_extras.json", orient="index")
extras["esg"] = extras["esg"].replace("", np.nan).astype(float)
df = df.merge(extras, left_on="company", right_index=True, how="left")


def calc_sentiment_polarity(row):
    return (row["n_positive_words"] - row["n_negative_words"]) / (row["n_positive_words"] + row["n_negative_words"])


df["sentiment_polarity"] = df.apply(calc_sentiment_polarity, axis=1)
df_ = df.groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_["year"], y=df_["sentiment"], mode="lines", name="All reports", line=dict(width=4)))

cc_ = df[df["sector"] == "Consumer Cyclical"].groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
fig.add_trace(go.Scatter(x=cc_["year"], y=cc_["sentiment"], mode="lines", name="Consumer Cyclical", line=dict(width=4)))

ind_ = df[df["sector"] == "Industrials"].groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
fig.add_trace(go.Scatter(x=ind_["year"], y=ind_["sentiment"], mode="lines", name="Industrials", line=dict(width=4)))

fin_ = (
    df[df["sector"] == "Financial Services"].groupby("year")["sentiment_polarity"].mean().reset_index(name="sentiment")
)
fig.add_trace(
    go.Scatter(x=fin_["year"], y=fin_["sentiment"], mode="lines", name="Financial Services", line=dict(width=4))
)

fig.update_layout(
    title_text="Average sentiment polarity of news articles by year (selected sectors)",
    title_x=0.5,
    title_y=0.92,
    title_font=dict(size=20),
    legend=dict(x=0.8, y=1, font=dict(size=20)),
    xaxis_title="year",
    yaxis_title="sentiment polarity",
    xaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=20), tickfont=dict(size=20)),
)
fig.show()
