from pathlib import Path

# load baier word list
with open(Path("esg_words", "baier.txt"), "r") as text_file:
    esg_words = text_file.readlines()
    esg_words = [w.rstrip().lower() for w in esg_words]

with open("sentiment/positive.txt", "r") as file:
    positive = file.read().splitlines()

with open("sentiment/negative.txt", "r") as file:
    negative = file.read().splitlines()

intersetion = set(negative).intersection(set(esg_words))
print(len(intersetion))
print(intersetion)

intersetion = set(positive).intersection(set(esg_words))
print(len(intersetion))
print(intersetion)
