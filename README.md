# 📄 DocuMind AI

DocuMind AI is a **Retrieval-Augmented Generation (RAG) based document assistant** that allows users to upload PDF documents and ask questions about their content.

The project was built to understand the core concepts behind **RAG, document processing, text chunking, embeddings, vector search, query rewriting, and LLM-based question answering**.

## 🚀 Live Demo

[Try DocuMind AI](https://documind-tgbfuiptg92xfh3exh279p.streamlit.app/)

## ✨ Features

- 📄 Upload one or multiple PDF documents
- 🔍 Extract text from PDF documents
- ✂️ Split documents into smaller overlapping chunks
- 🧠 Generate embeddings for document chunks
- 🔎 Perform semantic similarity search using FAISS
- 🤖 Generate answers using Google Gemini
- 🔄 Rewrite follow-up questions into standalone questions
- 💬 Support conversational question answering
- 📌 Display document, page, and chunk sources
- 🛡️ Restrict answers to information available in uploaded documents
- 🌐 Deploy using Streamlit Community Cloud

## 🧠 How It Works

DocuMind AI follows a standard RAG pipeline:

```text
PDF Document
     │
     ▼
Text Extraction
     │
     ▼
Text Chunking
     │
     ▼
Embeddings
     │
     ▼
FAISS Vector Store
     │
     ▼
Semantic Similarity Search
     │
     ▼
Relevant Document Chunks
     │
     ▼
RAG Prompt + Context
     │
     ▼
Google Gemini
     │
     ▼
Grounded Answer + Sources

DocuMind/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── utils/
    ├── chunker.py
    ├── document_registry.py
    ├── embeddings.py
    ├── llm.py
    ├── pdf_loader.py
    ├── prompts.py
    ├── qa_chain.py
    ├── query_rewriter.py
    └── vector_store.py
