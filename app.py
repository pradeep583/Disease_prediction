from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from main import getPrediction

from flask import flash
import os

#Save images to the 'static' folder as Flask serves images from this directory
UPLOAD_FOLDER = 'static'

#Create an app object using the Flask class. 
app = Flask(__name__, static_folder="static")
app.secret_key = "secret key"
#Define the upload folder to save images uploaded by the user. 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('client.html')


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

           
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            label = getPrediction(filename)
            # Flash the prediction and file path
            flash('Prediction: ')
            flash(label)
            flash(file_path)

            return render_template('client.html', prediction=label, image=file_path)
            
        else:
            flash('Allowed file types are png, jpg, jpeg')
            return redirect(request.url)



if __name__ == "__main__":
    app.run()