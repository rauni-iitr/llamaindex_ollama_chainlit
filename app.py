import os
import openai
import chainlit as cl
import yaml
import chromadb

from utils import *

@cl.on_chat_start
async def start():
    await cl.Avatar(
        name="Chatbot",
        url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4",
    ).send()
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
    Settings.callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
    file_paths = [x.path for x in files]
    # index = load_components(storage_path=persist_dir)
    index = ingest_docs(input_files=file_paths, storage_path=persist_dir, callback=Settings.callback_manager)
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)
    cl.user_session.set("query_engine", query_engine)

    # msg.content = "RAG is ready! please go ahead and ask questions."
    # await msg.update()
    await cl.Message(
        author="Assistant", content="RAG Ready.....\n\
            Hello! I am an AI Assistant. How may I help you?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")

    msg = cl.Message(content="", author="Assistant")

    # res = await cl.make_async(query_engine.query)(message.content)

    # for token in res.response_gen:
    #     await msg.stream_token(token)
    # await msg.send()

    res = query_engine.query(message.content)
    # print(type(res))
    answer = ''
    # print(answer)
    source = [x.text for x in res.source_nodes]
    text_elements = [cl.Text(content=x, name=f"Source_{i}") for i, x in enumerate(source)]

    for token in res.response_gen:
        await msg.stream_token(token)
    # await msg.send()

    if (text_elements):
        answer += "\nSources: {}".format(", ".join([x.name for x in text_elements]))
    else:
        answer += "\nNo Sources found."

    # msg.content = answer
    # # print(msg.content)
    # msg.elements = text_elements
    # await msg.send()
    await cl.Message(content=answer, author="Assistant", elements=text_elements).send()


