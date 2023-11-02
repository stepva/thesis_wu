from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv(Path("reports") / "reports_results.csv")
extras = pd.read_json(Path("common") / "company_extras.json", orient="index")
extras["esg"] = extras["esg"].replace("", np.nan).astype(float)
df = df.merge(extras, left_on="company", right_index=True)

print("Total number of reports:", len(df))

df_ = df.groupby("country")["company"].nunique().reset_index(name="counts")

fig = px.pie(df_, values="counts", names="country", hover_data=["counts"], labels={"counts": "count"})
fig.update_traces(textinfo="value", textfont_size=20)
fig.update_layout(
    title_text="Companies by country",
    title_x=0.5,
    title_font=dict(size=20),
    legend=dict(x=0.8, y=0.5, font=dict(size=20)),
)
# fig.show()

suffixes = ["ESG", "CSR", "INT", "NFI", "ENV", "CSR_ENV", "CSR_2", "SUS", "SR"]
df.loc[df["additional_info"].isin(suffixes), "report_type"] = "special"
df.loc[~df["additional_info"].isin(suffixes), "report_type"] = "normal"

print("Total number of special reports:", len(df[df["report_type"] == "special"]))

df_ = df.groupby(["year", "report_type"])["report"].size().reset_index(name="counts")

fig = go.Figure()

for spec in df_["report_type"].unique():
    df_sub = df_[df_["report_type"] == spec]
    fig.add_trace(
        go.Bar(
            x=df_sub["year"],
            y=df_sub["counts"],
            name=spec,
            text=df_sub["counts"],
            textposition="auto",
            textfont_size=20,
        )
    )

fig.update_layout(barmode="stack")
fig.update_layout(
    title_text="Number of reports by year",
    title_x=0.5,
    title_y=0.95,
    title_font=dict(size=40),
    legend=dict(x=0.915, y=0.1, font=dict(size=30)),
    xaxis_title="Year",
    yaxis_title="Count",
    xaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
    yaxis=dict(title_font=dict(size=30), tickfont=dict(size=20)),
)
fig.show()
