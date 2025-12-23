import streamlit as st
import os
from app import get_answer_from_file

st.title("RAG PDF Q&A")

uploaded = st.file_uploader("Upload file", type=["pdf","txt","docx","doc","md"])
query = st.text_input("Ask something from file")

if st.button("Get Answer"):
    if not uploaded:
        st.write("Upload a file first")
    elif not query:
        st.write("Enter a question")
    else:
        path = os.path.join("uploads", uploaded.name)
        with open(path, "wb") as f:
            f.write(uploaded.read())

        context, answer = get_answer_from_file(path, query)
        st.subheader("Context")
        st.write(context.replace("\n", " "))
        st.subheader("Answer")
        st.write(answer)

        os.remove(path)
