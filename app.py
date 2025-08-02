from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from sambar_check import check_sambar_consistency

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    filename = None

    if request.method == 'POST' and 'sambar_image' in request.files:
        img = request.files['sambar_image']
        if img.filename != '':
            filename = secure_filename(img.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(filepath)
            result = check_sambar_consistency(filepath)

    return render_template('index.html', result=result, filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

