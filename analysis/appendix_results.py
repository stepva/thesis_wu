from pathlib import Path
import pandas as pd
import numpy as np


reports_results = pd.read_csv(Path("reports") / "reports_results.csv")
extras = pd.read_json(Path("common") / "company_extras.json", orient="index")
extras.to_csv("companies_with_extras.csv", index=True)
extras["esg"] = extras["esg"].replace("", np.nan).astype(float)
reports_results = reports_results.merge(extras, left_on="company", right_index=True, how="left")

comp_years = (
    reports_results.groupby(["company", "year", "sector"])[
        [
            "n_pages",
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

comp_years["sentiment_polarity"] = (comp_years["n_positive_words"] - comp_years["n_negative_words"]) / (
    comp_years["n_positive_words"] + comp_years["n_negative_words"]
)
comp_years["sentiment_polarity_env"] = (comp_years["n_positive_words_env"] - comp_years["n_negative_words_env"]) / (
    comp_years["n_positive_words_env"] + comp_years["n_negative_words_env"]
)
comp_years["sentiment_polarity_soc"] = (comp_years["n_positive_words_soc"] - comp_years["n_negative_words_soc"]) / (
    comp_years["n_positive_words_soc"] + comp_years["n_negative_words_soc"]
)
comp_years["sentiment_polarity_gov"] = (comp_years["n_positive_words_gov"] - comp_years["n_negative_words_gov"]) / (
    comp_years["n_positive_words_gov"] + comp_years["n_negative_words_gov"]
)

comp_years.to_csv("appenidx_table_reports.csv", index=False)

comp_years = comp_years.groupby(["sector", "company"])[
    ["sentiment_polarity", "sentiment_polarity_env", "sentiment_polarity_soc", "sentiment_polarity_gov"]
].mean()
comp_years = (
    comp_years.groupby("sector")[
        ["sentiment_polarity", "sentiment_polarity_env", "sentiment_polarity_soc", "sentiment_polarity_gov"]
    ]
    .agg(["mean", "count"])
    .reset_index()
)
comp_years = comp_years.round(4)
comp_years.to_csv("appenidx_table_reports.csv")
