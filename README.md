**📄 DocuMind AI**

DocuMind AI is a Retrieval-Augmented Generation (RAG) based document assistant that allows users to upload PDF documents and ask questions about their content.

The project was built to understand the core concepts behind RAG, document processing, text chunking, embeddings, vector search, query rewriting, and LLM-based question answering.

**🚀 Live Demo**

Try DocuMind AI:

https://documind-tgbfuiptg92xfh3exh279p.streamlit.app/

**✨ Features**

📄 Upload one or multiple PDF documents
🔍 Extract text from PDF documents
✂️ Split documents into smaller overlapping chunks
🧠 Generate embeddings for document chunks
🔎 Perform semantic similarity search using FAISS
🤖 Generate answers using Google Gemini
🔄 Rewrite follow-up questions into standalone questions
💬 Support conversational question answering
📌 Display document, page, and chunk sources
🛡️ Restrict answers to information available in uploaded documents
🌐 Deploy using Streamlit Community Cloud

**🧠 How It Works**
DocuMind AI follows a standard RAG pipeline:

PDF Document
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Embedding Generation
     ↓
FAISS Vector Store
     ↓
User Question
     ↓
Query Rewriting
     ↓
Semantic Retrieval
     ↓
Relevant Document Context
     ↓
Google Gemini
     ↓
Source-Grounded Answer

For follow-up questions, the previous conversation is used to rewrite the question into a standalone query before performing retrieval.

**🛠️ Tech Stack**
Python, 
 Streamlit, 	
 PyPDF,     	
 LangChain,	     
 Sentence Transformers,	
 FAISS,	     
 Google Gemini,	
 python-dotenv	

**📁 Project Structure**

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
    
**🔄 RAG Pipeline**

1. PDF Upload

Users upload PDF documents through the Streamlit interface.

2. Text Extraction

The application extracts text from the uploaded PDF while preserving page information.

3. Text Chunking

The extracted content is divided into smaller overlapping chunks using a recursive text splitter.

Chunking allows the retrieval system to search for relevant sections rather than processing the entire document at once.

4. Embeddings

Each document chunk is converted into a numerical vector representation using a local embedding model.

5. FAISS Vector Store

The generated embeddings are stored in a FAISS vector index.

When a user asks a question, FAISS retrieves the chunks that are semantically most similar to the question.

6. Query Rewriting

Follow-up questions are rewritten into standalone questions using the conversation history.

For example:

User: What is BERT?

User: What are its two objectives?

The second question can be rewritten as:

What are BERT's two pre-training objectives?

This helps improve document retrieval for conversational questions.

7. Context Construction

The retrieved chunks are combined into a context containing:

Document name
Page number
Chunk content

8. Gemini Response

The retrieved context and user's question are sent to Google Gemini.

The prompt instructs the model to:

Use only the provided document context
Avoid outside information
Provide relevant source citations
Avoid inventing sources
State when the information cannot be found

**💻 Installation**

1. Clone the Repository
git clone https://github.com/Shlok4441/DocuMind.git
2. Navigate to the Project
cd DocuMind
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
macOS / Linux
source venv/bin/activate
Windows
venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt
6. Configure the Gemini API Key

Create a .env file in the project root:

GOOGLE_API_KEY=your_google_gemini_api_key

7. Run the Application
streamlit run app.py

The application will be available at:

http://localhost:8501

**🔑 Environment Variables**

The application requires a Google Gemini API key.

GOOGLE_API_KEY=your_api_key

Never commit your API key to GitHub.

The .env file is excluded using .gitignore.

**🧪 Example Questions**

After uploading a document, you can ask questions such as:

What is BERT?


What are the two pre-training objectives used by BERT?


What is BERT's masked language model objective?


What is Next Sentence Prediction in BERT?


How does BERT achieve bidirectional representations?

You can also ask follow-up questions based on previous conversations.

**📌 Source-Grounded Answers**

DocuMind AI provides source references along with retrieved information.

Example:

BERT uses two pre-training objectives: Masked Language
Model and Next Sentence Prediction [1].

The application also displays the corresponding document, page, and chunk used during retrieval.

**🛡️ Out-of-Document Questions**

DocuMind AI is designed to avoid using external knowledge when answering document-related questions.

If the requested information cannot be found in the uploaded documents, the application responds:

I couldn't find this information in the uploaded documents.

This helps keep generated responses grounded in the retrieved document context.

**🌐 Deployment**

DocuMind AI is deployed using Streamlit Community Cloud.

The Gemini API key is configured through Streamlit Secrets rather than being stored in the repository.

Example:

GOOGLE_API_KEY = "your_api_key"

**⚠️ Current Limitation**

The current version is primarily designed as a single-user/demo application.

The deployed version uses persistent application storage for the vector store and document registry. Therefore, documents uploaded to the deployed instance can be visible across sessions.

A production-ready multi-user implementation would isolate each user's documents and vector store by session or user ID.
**
🎯 Learning Objectives**

This project was developed to understand and implement:

Retrieval-Augmented Generation (RAG),
 PDF document ingestion,
 Text extraction,
 Recursive text chunking,
 Chunk overlap,
 Text embeddings,
 Vector databases,
 FAISS similarity search,
 Semantic retrieval,
 Prompt engineering,
 Query rewriting,
 Conversational question answering,
 Source attribution,
 LLM integration,
 Streamlit application development,
 Cloud deployment

**🔮 Future Improvements**

Possible improvements include:

👤 User authentication,
 🔐 User-specific document isolation,
 🗑️ Document deletion from the UI,
 🔎 Improved retrieval and reranking,
 📚 Support for additional file formats,
 💬 Conversation export,
 ⚡ Streaming responses,
 📊 Retrieval evaluation and performance metrics

**👨‍💻 Author**
Shlok Gawade
