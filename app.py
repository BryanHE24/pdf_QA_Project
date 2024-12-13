from flask import Flask, request, jsonify, render_template_string
from models.query_handler import query_pdf_with_better_context
from PyPDF2 import PdfReader
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', format='%(asctime)s - %(message)s')

# Read PDF utility function
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    logging.debug(f"Extracted text from {file_path}, length: {len(text)}")
    return text

# Split text into chunks
def split_text(text, chunk_size=500, overlap=100):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]
    logging.debug(f"Split text into {len(chunks)} chunks with chunk size {chunk_size} and overlap {overlap}")
    return chunks

# Routes
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF Query</title>
    </head>
    <body>
        <h1>PDF Query</h1>
        <form id="uploadForm" enctype="multipart/form-data" method="post" action="/upload">
            <label for="file">Upload PDF:</label>
            <input type="file" id="file" name="file" accept=".pdf" required><br><br>
            <label for="query">Enter your query:</label>
            <input type="text" id="query" name="query" required><br><br>
            <button type="submit">Submit</button>
        </form>
        <h2>Answer:</h2>
        <p id="answer">{{ answer }}</p>
    </body>
    </html>
    """, answer="")

@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        # Ensure file and query are in the request
        if 'file' not in request.files or 'query' not in request.form:
            return jsonify({"error": "File and query are required"}), 400

        file = request.files['file']
        query = request.form['query']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        logging.info(f"Uploaded file: {file.filename}")
        logging.info(f"Query received: {query}")

        # Process the PDF
        text = read_pdf(file_path)
        chunks = split_text(text)
        answer = query_pdf_with_better_context(query, chunks)

        logging.info(f"Generated answer: {answer}")

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PDF Query</title>
        </head>
        <body>
            <h1>PDF Query</h1>
            <form id="uploadForm" enctype="multipart/form-data" method="post" action="/upload">
                <label for="file">Upload PDF:</label>
                <input type="file" id="file" name="file" accept=".pdf" required><br><br>
                <label for="query">Enter your query:</label>
                <input type="text" id="query" name="query" required><br><br>
                <button type="submit">Submit</button>
            </form>
            <h2>Answer:</h2>
            <p id="answer">{{ answer }}</p>
        </body>
        </html>
        """, answer=answer)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
