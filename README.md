# 📘 RAG Document Question Answering System

A **Retrieval-Augmented Generation (RAG)** application that allows users to upload a document, ask questions, and receive answers grounded strictly in the document’s content.

This project demonstrates document chunking, embeddings, FAISS vector search, LLM answering, and grounding enforcement.

---

## 📂 Project Structure

```
app.py      → Core RAG logic
llm.py      → OpenRouter LLM API integration
prompt.py   → Prompt template for grounded answering
ui.py       → Streamlit user interface
```

---

## 🚀 How to Run

### 1️⃣ Install dependencies

```
uv sync
```

### 2️⃣ Set API Key

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=YOUR_KEY
```

### 3️⃣ Launch the app

```
streamlit run ui.py
```

---

## ✅ Models Used

### 🔹 Embedding Model

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Why this model?**

* Lightweight & fast
* Produces 384-dimensional embeddings
* Strong semantic understanding for QA
* Runs locally (no internet dependency)
* Ideal for academic & practical RAG systems

Embeddings are stored in **FAISS** for efficient retrieval.

---

### 🔹 LLM

**Provider:** OpenRouter
**Model:** `openai/gpt-4o-mini`

**Why this model?**

* Cost-efficient / often free
* Reliable contextual reasoning
* Works well with retrieval prompts
* Balanced accuracy & performance

The LLM only receives retrieved chunks — never the full document — ensuring **grounded answers only**.

---

## 🧩 RAG Pipeline

### 1️⃣ Text Extraction

* PDFs → processed with **PyPDF2**
* Other supported text formats → read directly

---

### 2️⃣ Chunking

```
chunk_size = 1000
chunk_overlap = 200
```

**Overlap** helps preserve continuity across chunks.

---

### 3️⃣ Embedding & Vector Storage

* Chunks embedded using MiniLM
* Stored in **FAISS vector store**
* Enables fast local semantic search

---

### 4️⃣ Semantic Retrieval

When a question is asked:

1️⃣ Query embedded
2️⃣ FAISS retrieves relevant chunks
3️⃣ Top-k chunks returned (typically k = 3–5)

Optional enhancements:

* Max-Marginal-Relevance to avoid duplicate chunks
* Similarity threshold to reject weak matches

---

## 🧠 Answer Generation (Grounded Only)

Prompt enforces grounding:

```
You are an assistant answering strictly using the provided context.
If the answer is not present, reply: "context not available".

Context:
<retrieved document chunks>

Question:
<user query>
```