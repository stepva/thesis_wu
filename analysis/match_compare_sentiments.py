from pathlib import Path
import time
import json
import pandas as pd


t = time.time()

news = pd.read_csv(Path("news") / "news_results.csv")
reports = pd.read_csv(Path("reports") / "reports_results.csv")
with open(Path("common") / "company_extras.json", "r") as json_file:
    extras = json.load(json_file)

companies = list(reports["company"].unique())

results = {}

excluded_fy = []
excluded_polarity = []

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
for company in companies:
    for year in years:
        reports_ = reports[(reports["company"] == company) & (reports["year"] == year)]
        reps_pos = reports_["n_positive_words"].sum()
        reps_neg = reports_["n_negative_words"].sum()

        if reps_pos + reps_neg < 1:
            excluded_polarity.append((company, year))
            continue

        reps_pol = (reps_pos - reps_neg) / (reps_pos + reps_neg)

        reps_ss_pols = {}
        for esg_ss in ["env", "soc", "gov"]:
            reps_pos_temp = reports_[f"n_positive_words_{esg_ss}"].sum()
            reps_neg_temp = reports_[f"n_negative_words_{esg_ss}"].sum()

            if reps_pos_temp + reps_neg_temp < 1:
                excluded_polarity.append((company, year, esg_ss))
                continue

            reps_ss_pols[esg_ss] = (
                reports_[f"n_positive_words_{esg_ss}"].sum() - reports_[f"n_negative_words_{esg_ss}"].sum()
            ) / (reports_[f"n_positive_words_{esg_ss}"].sum() + reports_[f"n_negative_words_{esg_ss}"].sum())

        news_ = news[(news["company"] == company) & (news["year"] == year)]

        if "fiscal_year" in extras[company].keys():
            news_pos = news_["n_positive_words_fy"].sum()
            news_neg = news_["n_negative_words_fy"].sum()
        else:
            news_pos = news_["n_positive_words"].sum()
            news_neg = news_["n_negative_words"].sum()

        if news_pos + news_neg < 1:
            excluded_polarity.append((company, year))
            continue

        news_pol = (news_pos - news_neg) / (news_pos + news_neg)

        news_ss_pols = {}
        for esg_ss in ["env", "soc", "gov"]:
            if "fiscal_year" in extras[company].keys():
                news_pos_temp = news_[f"n_positive_words_fy_{esg_ss}"].sum()
                news_neg_temp = news_[f"n_negative_words_fy_{esg_ss}"].sum()
            else:
                news_pos_temp = news_[f"n_positive_words_{esg_ss}"].sum()
                news_neg_temp = news_[f"n_negative_words_{esg_ss}"].sum()

            if news_pos_temp + news_neg_temp < 1:
                excluded_polarity.append((company, year, esg_ss))
                continue
            else:
                news_ss_pols[esg_ss] = (news_pos_temp - news_neg_temp) / (news_pos_temp + news_neg_temp)

        pol_diff = reps_pol - news_pol

        if company not in results.keys():
            results[company] = {}

        results[company][year] = {
            "reports_pol": reps_pol,
            "news_pol": news_pol,
            "pol_diff": pol_diff,
            "n_articles": int(news_["n_articles_processed"].sum()),
        }

        for esg_ss in ["env", "soc", "gov"]:
            if esg_ss not in news_ss_pols.keys():
                continue
            pol_diff = reps_ss_pols[esg_ss] - news_ss_pols[esg_ss]
            results[company][year][f"reports_pol_{esg_ss}"] = reps_ss_pols[esg_ss]
            results[company][year][f"news_pol_{esg_ss}"] = news_ss_pols[esg_ss]
            results[company][year][f"pol_diff_{esg_ss}"] = reps_ss_pols[esg_ss] - news_ss_pols[esg_ss]


with open(Path("results") / "match_compare_sentiments.json", "w") as json_file:
    json.dump(results, json_file)

print(excluded_fy)
print(excluded_polarity)

# todo fuckup variables, need to use the calcs themselves, this doesnt work
