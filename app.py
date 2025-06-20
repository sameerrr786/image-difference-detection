import os
import cv2
import numpy as np
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from utils import align_images

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['RESULT_FOLDER'] = 'static/results/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['RESULT_FOLDER']):
    os.makedirs(app.config['RESULT_FOLDER'])

def detect_changes(original_path, modified_path, output_path):
    original = cv2.imread(original_path)
    modified = cv2.imread(modified_path)
    
    if original is None or modified is None:
        return 0

    aligned_modified = align_images(original, modified)
    if aligned_modified is None:
        aligned_modified = modified

    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    aligned_modified_gray = cv2.cvtColor(aligned_modified, cv2.COLOR_BGR2GRAY)
    
    original_gray = cv2.GaussianBlur(original_gray, (5, 5), 0)
    aligned_modified_gray = cv2.GaussianBlur(aligned_modified_gray, (5, 5), 0)
    
    diff = cv2.absdiff(original_gray, aligned_modified_gray)
    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result = aligned_modified.copy()
    changes_detected = 0
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
            changes_detected += 1
            
    cv2.imwrite(output_path, result)
    return changes_detected

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_file = request.files['original']
        modified_file = request.files['modified']
        
        if original_file and modified_file:
            original_filename = secure_filename(original_file.filename)
            modified_filename = secure_filename(modified_file.filename)
            
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            modified_path = os.path.join(app.config['UPLOAD_FOLDER'], modified_filename)
            
            original_file.save(original_path)
            modified_file.save(modified_path)
            
            result_filename = "result_" + original_filename
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            
            changes = detect_changes(original_path, modified_path, result_path)
            
            return render_template('result.html',
                                   original_img=url_for('static', filename='uploads/' + original_filename),
                                   modified_img=url_for('static', filename='uploads/' + modified_filename),
                                   result_img=url_for('static', filename='results/' + result_filename),
                                   changes_detected=changes)
                                   
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 