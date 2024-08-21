## Chunker
- Most of things are handled by [MinerU](https://github.com/opendatalab/MinerU).
- MinerU extracts images and other image content.

1. Follow steps in this [repo](https://github.com/opendatalab/MinerU) to setup magic pdf and MinerU.
2. Set up required `.env` files
```
MILVUS_TOKEN=""
MILVUS_URI=""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_DEFAULT_REGION = ""
```
3. Run the `.ipynb` scripts in mentioned order.

---
Once `MinerU` is setup then execute this command to get results:
```
magic-pdf -p docs/trimmed_punch_manual.pdf -o output/ -m auto
```


## TODO
⬜️ Setup Github script to extract content from files.
