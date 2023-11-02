from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv(Path("news") / "news_results.csv")
extras = pd.read_json(Path("common") / "company_extras.json", orient="index")
extras.to_csv("companies_with_extras.csv", index=True)
extras["esg"] = extras["esg"].replace("", np.nan).astype(float)
df = df.merge(extras, left_on="company", right_index=True, how="left")


print("Number of news articles:")
print(df["n_articles_processed"].sum())

df_ = df.groupby(["year"])["n_articles_old"].sum().reset_index(name="counts")

fig = px.line(df_, x="year", y="counts", labels={"counts": "Count", "year": "Year"})
fig.update_traces(line=dict(width=4))
fig.update_layout(
    title_text="News articles by year",
    title_x=0.5,
    title_y=0.98,
    title_font=dict(size=40),
    legend=dict(x=0.8, y=0.5, font=dict(size=30)),
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()

comp_years = df.groupby(["company", "year"])[["n_articles_old"]].sum().reset_index()
df_ = comp_years.groupby("company")["n_articles_old"].sum().reset_index(name="counts")

counts, bins = np.histogram(df_["counts"], bins=20, range=(0, 2000))
bins_center = bins[:-1] + np.diff(bins) / 2

fig = go.Figure(
    data=[
        go.Bar(x=bins_center, y=counts, width=np.diff(bins), text=counts, textposition="auto", textfont_size=20)
    ]  # bin width
)

print(df_.sort_values(by="counts", ascending=False))

fig.update_layout(
    title_text="Histogram of companies and count of news articles",
    title_x=0.5,
    title_y=0.95,
    title_font=dict(size=40),
    legend=dict(x=0.8, y=0.5, font=dict(size=30)),
    xaxis_title="Number of news articles",
    yaxis_title="Number of companies",
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)

fig.show()


df = df.merge(df.groupby("sector")["company"].nunique().reset_index(name="sector_n"), on="sector")
df["sector_with_n"] = df["sector"] + " (" + df["sector_n"].astype(str) + ")"

df_ = df.groupby("sector_with_n")["n_articles_old"].mean().reset_index(name="counts")
fig = px.pie(df_, values="counts", names="sector_with_n", hover_data=["counts"], labels={"counts": "count"})
fig.update_traces(textinfo="value", textfont_size=20)
fig.update_layout(
    title_text="News articles by sector (with number of companies in parentheses)",
    title_x=0.5,
    title_font=dict(size=20),
    legend=dict(x=0.85, y=0.5, font=dict(size=20)),
)
fig.show()
