from flask import Flask, request, redirect, url_for, render_template
from threading import Thread
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def save_file(file_content, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename+'.png')
    with open(filepath, 'wb') as f:
        f.write(file_content)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file'] 
        filename = file.filename
        # filename = request.files['file'] 
        if file.filename == '':
            return 'No selected file'
        
        # Read file content into memory
        file_content = file.read()
        
        
        # Start a new thread to save the file
        thread = Thread(target=save_file, args=(file_content, filename))
        thread.start()
        # save_file(file_content, filename)
        return 'File is being uploaded in the background'
    return render_template('upload.html')

@app.route('/uploads')
def uploaded_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return '<br>'.join(files)

if __name__ == '__main__':
    app.run(debug=True)