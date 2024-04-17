import os
import openai
import chainlit as cl
import yaml
import chromadb

from utils import *

@cl.on_chat_start
async def start():
    files = None
    # Wait for the user to upload a PDF file
    while files is None:
        files = await cl.AskFileMessage(author="Assistant",
        content="Please upload a pdf/txt file to begin!",
        accept=["application/pdf", "text/plain"],
        max_size_mb=5, max_files=10
        ).send()
    # file = files[0]
    msg = cl.Message(author="Assistant", content=f"Processing …...",)
    await msg.send()

    file_paths = [x.path for x in files]
    # index = load_components(storage_path=persist_dir)
    index = ingest_docs(input_files=file_paths, storage_path=persist_dir)
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)
    cl.user_session.set("query_engine", query_engine)

    await cl.Message(
        author="Assistant", content="RAG Ready.....\n\
            Hello! I am an AI Virtual Assistant. How may I help you?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")

    msg = cl.Message(content="", author="Assistant")

    res = await cl.make_async(query_engine.query)(message.content)

    for token in res.response_gen:
        await msg.stream_token(token)
    await msg.send()

