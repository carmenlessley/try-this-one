# Write your code here :-)
import streamlit as st
from docx import Document
import re

st.set_page_config(page_title="Transcript Formatter", layout="wide")
st.title("Transcript Formatter")

uploaded_file = st.file_uploader("Upload your transcript (.txt)", type=["txt"])

def format_transcript(text):
    """
    Bold timestamps and speaker names, leave text normal.
    Assumes lines are in format: [00:01] SPEAKER: text
    """
    formatted_lines = []
    for line in text.split("\n"):
        match = re.match(r"(\[\d{2}:\d{2}\])\s*(.*?):\s*(.*)", line)
        if match:
            timestamp, speaker, content = match.groups()
            formatted_line = f"**{timestamp} {speaker}:** {content}"
        else:
            formatted_line = line  # lines that don't match keep as-is
        formatted_lines.append(formatted_line)
    return formatted_lines

if uploaded_file:
    transcript = uploaded_file.read().decode("utf-8")
    formatted_lines = format_transcript(transcript)

    # Display in Streamlit
    st.markdown("### Formatted Transcript")
    st.markdown("\n\n".join(formatted_lines))

    # Save to Word
    doc = Document()
    for line in formatted_lines:
        # Remove Markdown when writing to Word
        clean_line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        doc.add_paragraph(clean_line)
    doc_filename = "formatted_transcript.docx"
    doc.save(doc_filename)

    # Provide download button
    st.download_button(
        label="Download as Word Document",
        data=open(doc_filename, "rb"),
        file_name=doc_filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
