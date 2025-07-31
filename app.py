from flask import Flask, render_template, request, redirect, flash, after_this_request
from werkzeug.utils import secure_filename
from main import getPrediction
import os

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('client.html')

@app.route('/', methods=['POST'])
def submit_file():
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

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        label = getPrediction(filename)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
            except Exception as e:
                app.logger.error("Error deleting file: %s", e)
            return response

        return render_template('client.html', prediction=label, image=file_path)

    flash('Allowed file types are png, jpg, jpeg')
    return redirect(request.url)

if __name__ == "__main__":
    app.run()
