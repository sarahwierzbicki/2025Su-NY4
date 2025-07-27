from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.utils import secure_filename
import preprocessing_module

app = Flask(__name__)
import preprocessing_module

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#mongodb connection
client = MongoClient('mongodb://localhost:27017/')
db = client['name']
collection = db['data']

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
        
    resume_text = request.json.get("resume_text")    
    doc = process(resume_text)
    resume_data = {"parsed_resume": doc, "resumeID": 12345, }
    collection.insert_one(resume_data)
    #resume text will be returned and stored, find way to generate unique resume id  
#route for prediction
#in predict question fetching pasred text from unique resume id? or only 
@app.route('/predict_category', methods = ['GET']
def predict_category():
    try:
        data = request.get_json()
        resumeID = data.get('resumeID')

        resume_data = collection.find_one({'_id': resumeID})
        predict_resume = mongo_data.get('parsed_resume')
        input_data = {'inputs': parsed_resume)
        category_result = response
        return jsonify({'prediction': category_result}), 200
    except Exception as e:
        app.logger.error(f"Error during predicting: {e}")
        return jsonify({'error': "Error occured!"}), 500

#use category to search csv or dataframe and get matching jobs
    
