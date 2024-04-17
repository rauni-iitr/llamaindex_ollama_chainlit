# LLAMA-INDEX-OLLAMA-CHAINLIT-RAG

## About

This project runs a local llm agent based RAG model on LlamaIndex.

**LLM Used** : Ollama \
**Embedding** : HuggingFaceEmbeddings with llama-index \
**User Interface** : Chainlit

#### Note : Ollama runs on Linux or MacOS - automatically uses hardware accelerotor if available in this devices (GPU and MPS respectively), otherwise uses CPU

## Ollama setup on local device

### Mac
To install Ollama on a Mac, you need to have macOS 11 Big Sur or later. The installation process can be done in a few steps:
* **Download Ollama**: You can download Ollama for macOS from the official website.

* **Install with Homebrew**: If you prefer using Homebrew, you can install Ollama with the following command: \
    ```shell
    brew install ollama
    ```
* **Start Ollama** services on your mac, which runs on a local server which will serve all the api calls used in any llm application which will use Ollama:
    ```shell
    brew services start ollama
    ```

### Linux
For Linux users, the installation process is straightforward:

* **Install with a Single Command:** You can install Ollama using a single command by running in your terminal:
    ```shell
    curl https://ollama.ai/install.sh | sh
    ```

### Find a model to use: 
To find a model in Ollama, you can visit the [Ollama library](https://ollama.com/library?sort=popular) page. This page lists all the available models that you can pull and run locally using Ollama. 

### Download/Pull a model for Ollama:
```shell
ollama pull mistral:latest
```

Now, we are all set for writing our rag application in LlamaIndex. 

 **Note** : we can use downloaded gguf files from huggingface and use LLamaCPP or any other llm loader classes for gguf files instead of Ollama.

## Setup Enviornment




