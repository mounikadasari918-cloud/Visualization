import streamlit as st
import pdfplumber
import docx
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np
import re
import io

# 📄 Extract text from PDF using pdfplumber
def extract_text_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# 📄 Extract text from DOCX
def extract_text_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# 🧹 Basic text preprocessing without NLTK
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    return tokens

# ☁ Generate Word Cloud
def show_wordcloud(tokens):
    wc = WordCloud(width=800, height=400, background_color='white').generate(" ".join(tokens))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
    plt.clf()

# 📊 Word Frequency Bar Chart
def show_frequency(tokens):
    freq = Counter(tokens).most_common(20)
    words, counts = zip(*freq)
    plt.figure(figsize=(10, 4))
    sns.barplot(x=list(words), y=list(counts), palette='viridis')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.clf()

# 🥧 Word Frequency Pie Chart
def show_piechart(tokens):
    freq = Counter(tokens).most_common(10)
    words, counts = zip(*freq)
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=words, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.axis('equal')
    st.pyplot(plt)
    plt.clf()

# 🚀 Streamlit UI
st.title("📚 Text Visualization App")
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()
    raw_text = ""

    try:
        if file_type == "pdf":
            raw_text = extract_text_pdf(io.BytesIO(uploaded_file.read()))
        elif file_type == "docx":
            raw_text = extract_text_docx(uploaded_file)
        else:
            st.error("Unsupported file format.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

    if raw_text:
        st.subheader("Extracted Text Preview")
        st.write(raw_text[:1000] + "...")  # Show preview

        tokens = preprocess_text(raw_text)

        option = st.selectbox("Choose Visualization", ["Word Cloud", "Word Frequency", "Pie Chart"])

        if option == "Word Cloud":
            show_wordcloud(tokens)
        elif option == "Word Frequency":
            show_frequency(tokens)
        elif option == "Pie Chart":
            show_piechart(tokens)
    else:
        st.warning("No text could be extracted from the file.")
