import streamlit as st
import PyPDF2
import spacy

st.title("📄 AI-Powered Resume Analyzer")

# Upload the resume PDF
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    # Extract text from the PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    st.subheader("📝 Extracted Resume Text")
    st.write(text)

    # Load NLP model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Named Entity Recognition (NER)
    st.subheader("🔍 Named Entities Found")
    for ent in doc.ents:
        st.markdown(f"- **{ent.label_}**: {ent.text}")

    # Job description input
    job_desc = st.text_area("💼 Paste a Job Description")

    if job_desc:
        job_doc = nlp(job_desc)
        resume_tokens = set([token.lemma_.lower() for token in doc if token.is_alpha])
        job_tokens = set([token.lemma_.lower() for token in job_doc if token.is_alpha])
        match = resume_tokens.intersection(job_tokens)

        st.subheader("📌 Matching Keywords")
        st.write(match)

        st.markdown(f"✅ **Match Score**: `{len(match)} / {len(job_tokens)}`")
