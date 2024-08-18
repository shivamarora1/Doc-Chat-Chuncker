### * Script to insert content in vector database.
### * Script assumes data is stored in .csv file.

from pymilvus import connections, Collection
from pymilvus import utility, FieldSchema, CollectionSchema, DataType, Collection
from dotenv import load_dotenv
import os
import utils

load_dotenv()

CSV_FILE_LINK = "../data/extracted_content.csv"
COLLECTION_NAME = "rag_vs"

MILVUS_TOKEN = os.getenv("MILVUS_TOKEN")
MILVUS_URI = os.getenv("MILVUS_URI")
DIMENSION = 384
BATCH_SIZE = 128

collection: Collection = None

### Creating a collection
connections.connect(uri=MILVUS_URI, token=MILVUS_TOKEN)

if not utility.has_collection(collection_name=COLLECTION_NAME):
    print(f"collection {COLLECTION_NAME} not found. creating one.")
    fields = [
        FieldSchema(
            name="id", dtype=DataType.INT64, is_primary=True, auto_id=True
        ),  # id is auto=increment
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
        FieldSchema(name="page_num", dtype=DataType.INT64),
        FieldSchema(name="image_url", dtype=DataType.VARCHAR, max_length=500),
    ]
    schema = CollectionSchema(fields=fields)
    collection = Collection(name=COLLECTION_NAME, schema=schema)

    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1536},
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()
else:
    print(f"collection {COLLECTION_NAME} already exists.")
    collection = Collection(name=COLLECTION_NAME)


def insert_data(data):
    embeddings = utils.generate_embeddings(data[0])
    ins = [
        data[0],
        embeddings,
        data[1],
        data[2],
    ]
    collection.insert(ins)


data_batch = [[], [], []]

count = 0

for content, page_num, image_url in utils.csv_load(CSV_FILE_LINK):
    print(page_num)
    data_batch[0].append(content)
    data_batch[1].append(int(page_num))
    data_batch[2].append(image_url)
    if len(data_batch[0]) % BATCH_SIZE == 0:
        insert_data(data_batch)
        data_batch = [[], [], []]
        print(f"\ninserted... {count} contents")
    count += 1

if len(data_batch[0]) != 0:
    insert_data(data_batch)

collection.flush()
