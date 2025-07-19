from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
import preprocessing_module

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#load spacy model
try:
    nlp = spacy.load("en_core_web_sm")  
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Downloading...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

#process resume
@app.route('/process_resume', methods=['POST'])
def process_resume():
    if 'file' not in request.files:
        return jsonify({'error': "No file"}), 400
    
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        resume_text = ""
        if filename.lower().endswith('.pdf'):
            resume_text = get_pdf_text(file_path)
        elif filename.lower.endswith('.docx'):
            resume_text = get_docx_text(file_path)
        else:
            return jsonify({"Error": "Unsupported file type. Please upload either PDF or DOCX format."}), 400

        os.remove(file_path)

        return jsonify({resume_text}), 200

    #resume text will be returned and stored, find way to generate unique resume id  



