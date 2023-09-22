import streamlit as st
import os
import sqlite3
from datetime import datetime

# Create the uploads folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create the SQLite database
conn = sqlite3.connect('db.sqlite')
conn.execute('''
   CREATE TABLE IF NOT EXISTS files (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       filename TEXT,
       filesize TEXT,
       uploaded_on TEXT,
       format TEXT,
       path TEXT
   )
''')
conn.close()

def upload_file():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_contents = uploaded_file.read()  # Read file contents
        filename = uploaded_file.name

        # Save the file to the uploads folder
        with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
            f.write(file_contents)

        file_size = len(file_contents)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        upload_timestamp = datetime.now().strftime('%d %B %Y')

        file_format = filename.split('.')[-1]

        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO files (filename, filesize, uploaded_on, format, path) VALUES (?, ?, ?, ?, ?)",
                       (filename, f'{file_size_mb} MB', upload_timestamp, file_format.upper(), os.path.join(UPLOAD_FOLDER, filename)))
        conn.commit()
        conn.close()

        st.success(f"File '{filename}' uploaded successfully!")

def get_metadata():
    st.subheader("Retrieve File Metadata")
    filename = st.text_input("Enter filename:")
    if st.button("Get Metadata"):
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files WHERE filename=?", (filename,))
        result = cursor.fetchone()
        conn.close()

        if result:
            st.write("Metadata:")
            st.write(f"Filename: {result[1]}")
            st.write(f"Filesize: {result[2]}")
            st.write(f"Uploaded On: {result[3]}")
            st.write(f"Format: {result[4]}")
            st.write(f"Path: {result[5]}")
        else:
            st.warning("File not found")

st.title("File Ingestion and Metadata Retrieval")
upload_file()
get_metadata()
