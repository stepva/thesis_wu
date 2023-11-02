from pathlib import Path
import json
from collections import defaultdict
from wordcloud import WordCloud

sentiment_words_path = Path("reports") / "report_sentiment_words.json"

with open(sentiment_words_path, "r") as json_file:
    sentiment_words = json.load(json_file)

rep_all_positives = defaultdict(int)
rep_all_negatives = defaultdict(int)
for comp, reports in sentiment_words.items():
    for rep, words in reports.items():
        for k, v in words["positive_words"].items():
            rep_all_positives[k] += v
        for k, v in words["negative_words"].items():
            rep_all_negatives[k] += v

# print("reports positives")
# print(sum(rep_all_positives.values()))
# print(len(rep_all_positives.keys()))

# print("reports negatives")
# print(sum(rep_all_negatives.values()))
# print(len(rep_all_negatives.keys()))

WordCloud(background_color="white").generate_from_frequencies(frequencies=rep_all_positives).to_file(
    "results/reports_positive_wordcloud.png"
)

WordCloud(background_color="white").generate_from_frequencies(frequencies=rep_all_negatives).to_file(
    "results/reports_negative_wordcloud.png"
)

sentiment_words_path = Path("news") / "news_sentiment_words.json"

with open(sentiment_words_path, "r") as json_file:
    sentiment_words = json.load(json_file)

all_positives = defaultdict(int)
all_negatives = defaultdict(int)
for comp, reports in sentiment_words.items():
    for rep, words in reports.items():
        if "positive_words" not in words.keys():
            continue
        for k, v in words["positive_words"].items():
            all_positives[k] += v
        for k, v in words["negative_words"].items():
            all_negatives[k] += v


# print("news positives")
# print(sum(all_positives.values()))
# print(len(all_positives.keys()))

# print("news negatives")
# print(sum(all_negatives.values()))
# print(len(all_negatives.keys()))


# print("news and reports positives intersection")
# print(len(set(all_positives.keys()).intersection(set(rep_all_positives.keys()))))

# print("news and reports negatives intersection")
# print(len(set(all_negatives.keys()).intersection(set(rep_all_negatives.keys()))))


WordCloud(background_color="white").generate_from_frequencies(frequencies=all_positives).to_file(
    "results/news_positive_wordcloud.png"
)

WordCloud(background_color="white").generate_from_frequencies(frequencies=all_negatives).to_file(
    "results/news_negative_wordcloud.png"
)
