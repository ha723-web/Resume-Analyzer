import streamlit as st
import PyPDF2
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Add custom CSS styles for the header and text
st.markdown("""
    <style>
        .big-font {
            font-size:50px !important;
            color: #3E8E41;
        }
        .small-font {
            font-size:20px !important;
            color: #FF6F61;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">📄 AI-Powered Resume Analyzer</p>', unsafe_allow_html=True)

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

    # Add Download Button for the extracted text
    st.download_button(
        label="Download Extracted Text",
        data=text,
        file_name="extracted_resume.txt",
        mime="text/plain"
    )

    # Generate word cloud from the resume text
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Display the word cloud
    st.subheader("💬 Most Frequent Keywords")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # Load NLP model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Named Entity Recognition (NER)
    st.subheader("🔍 Named Entities Found")

    # Initialize entity_dict with all possible labels
    entity_dict = {
        'PERSON': [],
        'ORG': [],
        'GPE': [],
        'DATE': [],
        'PRODUCT': [],
        'MONEY': [],
        'CARDINAL': [],
        'QUANTITY': []
    }

    for ent in doc.ents:
        if ent.label_ in entity_dict:
            entity_dict[ent.label_].append(ent.text)

    # Display the named entities by category
    for entity_type, entities in entity_dict.items():
        if entities:
            st.markdown(f"### {entity_type}")
            for entity in entities:
                st.markdown(f"- {entity}")

    # Job description input
    job_desc = st.text_area("💼 Paste a Job Description")

    if job_desc:
        # Process the job description
        job_doc = nlp(job_desc)
        resume_tokens = set([token.lemma_.lower() for token in doc if token.is_alpha])
        job_tokens = set([token.lemma_.lower() for token in job_doc if token.is_alpha])

        # Keyword matching
        match = resume_tokens.intersection(job_tokens)

        # Calculate match percentage safely
        match_score = len(match) / len(job_tokens) * 100 if len(job_tokens) > 0 else 0

        st.subheader("📌 Matching Keywords")
        st.write(match)

        # Score out of 100
        st.markdown(f"### 🎯 **Resume Match Score: {match_score:.2f} / 100**")

        # Rating Level
        if match_score >= 85:
            rating = "🌟 Excellent Fit"
        elif match_score >= 70:
            rating = "✅ Good Fit"
        elif match_score >= 50:
            rating = "⚠️ Average Fit"
        else:
            rating = "❗ Needs Improvement"

        st.markdown(f"### {rating}")

        # Suggestions for Improvement
        st.subheader("🛠 Suggestions to Improve Your Resume")

        suggestions = []

        if match_score < 85:
            missing_keywords = job_tokens - resume_tokens
            if missing_keywords:
                suggestions.append(f"🔍 Add these keywords to align better with the job: `{', '.join(list(missing_keywords)[:10])}`")

        if not entity_dict['PERSON']:
            suggestions.append("👤 Include your name and personal details (No 'PERSON' entity found).")

        if not entity_dict['ORG']:
            suggestions.append("🏢 Mention organizations or companies you've worked at (No 'ORG' entity found).")

        if not entity_dict['DATE']:
            suggestions.append("📅 Include dates to show experience duration and achievements.")

        if not suggestions:
            st.success("✅ Your resume looks well-aligned with the job description!")
        else:
            with st.expander("📋 Click to View Resume Improvement Suggestions"):
                for tip in suggestions:
                    st.markdown(tip)

        # Display relevant skills from job description
        relevant_skills = job_tokens.intersection(resume_tokens)
        if relevant_skills:
            st.subheader("🔑 Relevant Skills for the Job Description")
            st.write(", ".join(relevant_skills))
        else:
            st.write("No relevant skills found.")
