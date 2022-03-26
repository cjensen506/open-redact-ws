import os
import flask
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import requests


app = Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            files_upload = {'file': (file.filename, file, 'application/pdf')}
            response = requests.post('https://open-redact-ipyrwuqhaq-wn.a.run.app/redact_pdf', files=files_upload, stream=True)
            if response.status_code == 200:
                flash('File successfully uploaded')
                return flask.send_file(response.raw, mimetype='application/pdf', as_attachment=False, download_name='redacted.pdf')
            else:
                flask.abort(response.status_code)
        else:
            flash('Allowed file types are pdf')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)
