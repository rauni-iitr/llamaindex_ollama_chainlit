import os
from typing import Dict, List
import chromadb
import yaml
import chainlit as cl

from llama_index.core.callbacks.base import CallbackManager
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings, VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter

TV_PKL_PATH = None
CHUNK_SIZE = None
CHUNK_OL = None
context_window = None
embed_model_name = None
nodes_path = None
bm25_pkl = None
persist_dir = None
data_read_path = None

with open('./config.yml', 'r') as file:
    var = yaml.safe_load(file)
# print(var)
globals().update(var)

Settings.llm = Ollama(model='mistral',
              request_timeout=100.0, 
              context_window=context_window)
Settings.context_window = context_window
Settings.embed_model = HuggingFaceEmbedding(model_name=embed_model_name, device='mps')
Settings.chunk_overlap = CHUNK_OL
Settings.chunk_size = CHUNK_SIZE
Settings.node_parser = TokenTextSplitter(chunk_size=Settings.chunk_size, chunk_overlap=Settings.chunk_overlap, separator=" ")

def ingest_docs(input_files, storage_path=persist_dir, callback = CallbackManager()):
    Settings.callback_manager = callback
    docs = SimpleDirectoryReader(input_files=input_files).load_data()
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    db = chromadb.PersistentClient(path=storage_path)
    chroma_collection = db.get_or_create_collection('quickstart')
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    vector_index = VectorStoreIndex.from_documents(documents=docs, storage_context=storage_context)
    print('docs_ingested')
    return vector_index

def load_components(storage_path=persist_dir):
    # service_context = ServiceContext.from_defaults(llm=Settings.llm, embed_model=Settings.embed_model)
    db = chromadb.PersistentClient(path=storage_path)
    chroma_collection = db.get_collection('quickstart')
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    # query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)

    return index

# print(data_read_path, persist_dir)
# query_engine = load_components()

# print(query_engine.query("What are the damages on tail bearing lug?").print_response_stream())
