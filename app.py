from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from main import getPrediction
import os

UPLOAD_FOLDER = 'static'
 

app = Flask(__name__, static_folder="static")
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('client.html')

#Add Post method to the decorator to allow for form submission. 
@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Save the uploaded image
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

    
            label = getPrediction(filename)

            flash(label)
            flash(file_path)

            return render_template('client.html', prediction=label, image=file_path)


if __name__ == "__main__":
    app.run()
