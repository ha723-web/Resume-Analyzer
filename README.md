# AI-Powered Resume Analyzer

## Overview
This application is an AI-powered resume analyzer that extracts text from resumes (PDF format), performs Named Entity Recognition (NER) to identify key information (such as personal details, skills, job titles, etc.), and compares the extracted resume with a job description to highlight matching keywords and relevant skills.

## Features
- Upload and extract text from resume PDF files.
- Perform Named Entity Recognition (NER) to identify entities such as persons, organizations, locations, etc.
- Compare job descriptions with resumes and display matching keywords.
- Generate a word cloud of the most frequent keywords in the resume.
- Download the extracted text from the resume.

## Requirements
Before running the application, ensure that you have the following Python libraries installed:

- streamlit
- PyPDF2
- spacy
- wordcloud
- matplotlib

You can install these requirements using the following command:

```bash
pip install -r requirements.txt

