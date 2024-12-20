import io
import os
import hashlib
import dropbox
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import chardet
from docx import Document

# Dropbox Authentication
DROPBOX_ACCESS_TOKEN = "sl.u.AFYqszT2lbhwmIdfS2-Osddf_Q946FzcLnB8YKWkXc94wXkFzrX9dNX_5Em_iLywo_fv7vSlQrX7x6SV0e85INYrdh84YAzZdvhmLKfUzV6C6_f0wVU6sDtZv_5ijbxvE6ALMwlk8DcQsVo3nusCsyztrr3xuEsMIBuNJtkVoaDVyI6HnTbQbDDJus3h2dO2z6UuYJwX_i35Iv1_xYVSLypg8oTWCMRBEnd-JHTf6-gVUN641B1HSHCmfonPKfud_y947Y-KHerfmdR9OiA6g0YWBdK1C-V_I5VSHlRzv5JhXdsWnn_5Yl_TVElrkzuOlRjh9irBRct21ZF9yN_EFm69dN8frISt_eWw0llLxn8XXJk8ERwq6WaNwBsEsgP-xKfDpPjMmXbOJycocIWuWPhE6LPAzfzpgplADn0TVUFznPFDzkoS4wund59OYW5dzHtBB4bXn26TuhDc0Lv9ivZc0yqw_EdsOuu3NwCOCuOL-VeGrmmmOJhmtLVhPc9bmLblBdzplQ1Acqmc_Y5o4iT117iEvCJhr3vrxjvWAmj5nm_ichd_LqTixupRrlxMZA6QiiSXZQBryubLg_BrW8JDQs_bfmgw8YzTvsgXKJOFSMMOSl_OrSzvOwpxWE7FdO84JsGL3bsOzJcHRkjA56rtYdAn7DQRvAiX7F5P0Ui3Vr5ZNgcCI99XyuLUNk9M1vtqFlrvz2nbzRwj9OeVC1s9m9UsBzwbMM-cRGBWqVu4p92bc8H1VVUDmxteWr1P0SCbnVuFy14t6HFRocc-ms0P1Mo6NGfpe9SoZQqTJWWdGwlGi5FfsC_A48UK0az3TbrqcBMY3W1BX3PlzM3Ge8vljAkUwoANK1Q_sd_b1YcfbfYBFfunnPmdWqQzUFhHS6nnK-7Xb_2BKDkMN2SOirCALbUSxJ7g2O4GKGeSHyQ9Zrb3McRRowosdyIzMPBE9jr8ANlS6ruPWAyjSzpJmr8Ao5uLSLaPuv6US-8GnlNnwHLzKlMwSsQZLbF981tztYBJst1hrZGvnNvEDhjsWl7zx1NNyN2R-VkucMt1TS2iG6KR8mWUTPwtehdADIOEHpe0WpwCKT_SXP2mNNStiJG-QlmYGWdYvvwFT_hE7e1vKUu0TrcHyabXkWPw0CESaE1EO3l17yaflOEhzs4S-AxoPZWyrbR7OwTkiL7RZtyOZJG4oz2ElCRQeoDb-HVGlFVTBzaQO9om11oq5XjbuKfOzX9ULEQ19Ljpi4OvcPBwkw99PEptBBVCe0UXIIPlOq6ONRkXXaX2YiY-c1Qi_kAT5J8-eKG4iZpO8DziO_qZj8crriykbo3Y54H4HtvgfA6trAShI81AEaNjQgFTeP9STAaKTTGBiNquUCuN-5HPoA4i7IDG1ov7uhjW4rssIiGWVvRhMQL0hLJaycgyFMA5frrNe87B2CxnR8xmTSk4wg"  # Replace with your actual Dropbox access token
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

def list_dropbox_files():
    """Retrieve file list from Dropbox."""
    files = []
    result = dbx.files_list_folder("", recursive=True)
    files.extend(result.entries)
    
    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)
        files.extend(result.entries)
    
    file_details = []
    for entry in files:
        if isinstance(entry, dropbox.files.FileMetadata):
            file_details.append({
                "name": entry.name,
                "path": entry.path_display,
                "size": entry.size,
                "type": entry.name.split('.')[-1] if '.' in entry.name else 'unknown'
            })
    return pd.DataFrame(file_details)


def categorize_files(files_df):
    """Categorize files based on extensions and NLP analysis."""
    categories = {
        "Documents": ["txt", "docx", "pdf"],
        "Media": ["jpg", "png", "mp4"],
        "Code": ["py", "java", "cpp"]
    }
    # Check if 'type' column exists before categorizing
    if "type" not in files_df.columns:
        print("Error: 'type' column not found in files_df.")
    else:
        files_df["category"] = files_df["type"].apply(
            lambda ext: next((cat for cat, exts in categories.items() if ext in exts), "Others")
        )
    return files_df


def summarize_text(file_path):
    """Generate a summary for a text or .docx file."""
    _, res = dbx.files_download(file_path)
    
    # Check if the file is a .docx file
    if file_path.endswith(".docx"):
        # Handle .docx files using python-docx
        doc = Document(io.BytesIO(res.content))
        text = " ".join([para.text for para in doc.paragraphs])  # Combine all paragraphs
    else:
        # Handle text files and detect encoding
        detected_encoding = chardet.detect(res.content)["encoding"]
        
        try:
            # Attempt to decode using the detected encoding
            text = res.content.decode(detected_encoding)
        except UnicodeDecodeError:
            # Fallback to UTF-8 or ignore errors
            text = res.content.decode("utf-8", errors="ignore")
    
    # Use Spacy NLP model to process the text and generate a summary
    doc_nlp = nlp(text)
    summary = " ".join([sent.text for sent in doc_nlp.sents][:2])  # First two sentences as summary
    return summary


def detect_duplicates(files_df):
    """Detect duplicate files based on hashes."""
    hashes = {}
    duplicates = []
    for _, row in files_df.iterrows():
        _, res = dbx.files_download(row["path"])
        file_hash = hashlib.md5(res.content).hexdigest()
        if file_hash in hashes:
            duplicates.append((row["path"], hashes[file_hash]))
        else:
            hashes[file_hash] = row["path"]
    return duplicates

def visualize_distribution(files_df):
    """Visualize file distribution across categories."""
    category_counts = files_df["category"].value_counts()
    category_counts.plot(kind="bar")
    plt.title("File Distribution by Category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.tight_layout()
    st.pyplot()

# Streamlit Interface
st.title("AI-Powered File Organizer")

# Fetch and display Dropbox files
st.header("Dropbox Files")
files_df = list_dropbox_files()

# Check if 'path' and other columns exist in files_df
print("Columns in files_df:", files_df.columns)
print("First few rows of files_df:", files_df.head())  # To verify the content

# Check if we have the 'path' column
if "path" in files_df.columns:
    st.dataframe(files_df)
else:
    st.write("Error: No 'path' column found in the file list.")

# Categorize files
if not files_df.empty:
    files_df = categorize_files(files_df)
else:
    st.write("No files found in your Dropbox.")

# Text Summarization
st.header("Text Summarization")
# Ensure we're selecting only files with 'Documents' category
if not files_df.empty and "category" in files_df.columns:
    text_file = st.selectbox(
        "Select a text file to summarize:",
        files_df[files_df["category"] == "Documents"]["path"].values  # Access path column
    )

    if st.button("Summarize"):
        summary = summarize_text(text_file)
        st.write(f"Summary: {summary}")
else:
    st.write("No documents found to summarize.")

# Duplicate Detection
st.header("Duplicate Detection")
if st.button("Detect Duplicates"):
    duplicates = detect_duplicates(files_df)
    if duplicates:
        st.write("Duplicates Found:")
        st.write(duplicates)
    else:
        st.write("No duplicates found.")

# Folder Visualization
st.header("Folder Visualization")
if st.button("Visuali;ze Distribution"):
    visualize_distribution(files_df)
