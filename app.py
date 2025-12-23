from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from prompt import DEFAULT_PROMPT
from llm import get_response

DATABASE_PATH = "database"

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "")
    return text

def extract_text_from_file(path):
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def store_text(text):
    chunks = chunk_text(text)
    embeddings = get_embeddings()
    db = FAISS.from_texts(chunks, embedding=embeddings)
    db.save_local(DATABASE_PATH)
    return db

def load_vectorstore():
    embeddings = get_embeddings()
    return FAISS.load_local(
        DATABASE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

def get_answer_from_file(file_path, query):
    text = extract_text_from_file(file_path)

    # build DB (overwrite per file for now)
    store_text(text)

    db = load_vectorstore()
    docs = db.similarity_search(query, k=5)

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
{DEFAULT_PROMPT}

Context:
{context}

Question:
{query}
"""

    return context, get_response(prompt)
