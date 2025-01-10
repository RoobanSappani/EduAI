from langchain.embeddings import HuggingFaceEmbeddings

EMBEDDINGS_MODEL = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")