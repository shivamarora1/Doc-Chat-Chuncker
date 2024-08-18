import csv
from sentence_transformers import SentenceTransformer

transformer = SentenceTransformer("all-MiniLM-L6-v2")


def csv_load(file):
    with open(file, newline="") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if "" in (row[0], row[1], row[2]):
                continue
            yield (row[0], row[1], row[2])


def generate_embeddings(data: list[str]):
    embeddings = transformer.encode(data)
    return [x for x in embeddings]
