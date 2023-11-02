from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

reports_results = pd.read_csv(Path("news") / "news_results.csv")

comp_years = (
    reports_results.groupby(["company", "year"])[
        [
            "n_sentences",
            "n_esg_sentences",
            "n_esg_sentences_env",
            "n_esg_sentences_soc",
            "n_esg_sentences_gov",
            "n_positive_words",
            "n_negative_words",
        ]
    ]
    .sum()
    .reset_index()
)
comp_years["esg_ratio"] = comp_years["n_esg_sentences"] / comp_years["n_sentences"]
comp_years["esg_ratio_env"] = comp_years["n_esg_sentences_env"] / comp_years["n_sentences"]
comp_years["esg_ratio_soc"] = comp_years["n_esg_sentences_soc"] / comp_years["n_sentences"]
comp_years["esg_ratio_gov"] = comp_years["n_esg_sentences_gov"] / comp_years["n_sentences"]

print(comp_years["esg_ratio"].mean())

print(comp_years["esg_ratio_env"].mean())


fig = go.Figure()
df_env = comp_years.groupby("year")["esg_ratio_env"].mean().reset_index(name="ratio")
fig.add_trace(go.Scatter(x=df_env["year"], y=df_env["ratio"], mode="lines", name="Environmental", line=dict(width=4)))

df_soc = comp_years.groupby("year")["esg_ratio_soc"].mean().reset_index(name="ratio")
fig.add_trace(go.Scatter(x=df_soc["year"], y=df_soc["ratio"], mode="lines", name="Social", line=dict(width=4)))

df_gov = comp_years.groupby("year")["esg_ratio_gov"].mean().reset_index(name="ratio")
fig.add_trace(go.Scatter(x=df_gov["year"], y=df_gov["ratio"], mode="lines", name="Governance", line=dict(width=4)))

fig.update_layout(
    title_text="Average ratio of ESG-to-all sentences of news by year (split by ESG category)",
    title_x=0.5,
    title_y=0.95,
    title_font=dict(size=40),
    legend=dict(x=0.85, y=0.35, font=dict(size=30)),
    xaxis_title="Year",
    yaxis_title="Ratio",
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()
