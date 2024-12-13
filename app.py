from flask import Flask, request, jsonify, render_template_string
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

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
