# 📘 RAG Document Question Answering System

This project implements a **Retrieval-Augmented Generation (RAG)** system that allows users to upload a document, ask questions, and receive answers grounded strictly in the content of that document. It demonstrates document chunking, embeddings, FAISS vector search, LLM answering, and grounding enforcement.

---

### File structure

app.py - contains all the logic
llm.py - code to call openrouter api
prompt.py - contains prompt
ui.py - contains streamlit ui

### Run the app
To run simply excecute '''uv sync'''
create a .env file with '''OPENROUTER_API_KEY=KEY'''
then '''streamlit run ui.py'''

## ✅ Models Used

### 🔹 Embedding Model

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Reason for choice**

* Lightweight and fast
* Produces 384-dimensional sentence embeddings
* Strong semantic understanding for QA tasks
* Works locally (no internet dependency)
* Ideal for academic RAG implementations

This model converts document chunks into vector embeddings which are stored and used for retrieval.

---

### 🔹 LLM

**Provider:** OpenRouter
**Model:** `openai/gpt-4o-mini`

**Reason for choice**

* Free / cost-efficient
* Reliable contextual reasoning
* Works well with retrieval-based prompts
* Good balance of speed and accuracy

The LLM never sees the entire document — only retrieved relevant chunks — ensuring grounded responses.

---

## 🧩 Document Chunking & Retrieval Pipeline

### 1️⃣ Text Extraction

* PDF files → processed using **PyPDF2**
* Other supported text formats → read directly

---

### 2️⃣ Chunking

Documents are split into chunks using:

```
chunk_size = 1000
chunk_overlap = 200
```

**Why overlap?**
To preserve continuity across chunks and avoid losing important context.

---

### 3️⃣ Embedding + Vector Storage

* Each chunk is embedded using `all-MiniLM-L6-v2`
* Stored in a **FAISS vector store**

FAISS enables fast and efficient semantic similarity search on local machine (no external vector DB).

---

### 4️⃣ Semantic Retrieval

When a user asks a question:
1️⃣ Query is embedded
2️⃣ FAISS finds most relevant document chunks
3️⃣ Top-k chunks (typically k = 3–5) are retrieved

Optional improvements applied:

* Max-Marginal-Relevance retrieval to avoid duplicate chunks
* Similarity threshold to reject weak matches

---

## 🧠 LLM Answer Generation

The LLM is not allowed to use outside knowledge.

A structured prompt is sent:

```
You are an assistant answering strictly using the provided context.
If the answer is not present, reply: "context not available".

Context:
<retrieved document chunks>

Question:
<user query>
```

The model then generates an answer **only based on retrieved content**.

---
### ✔ Transparency & Explainability

The system clearly displays:
1️⃣ Retrieved Context Chunks used
2️⃣ Final LLM Answer

---
