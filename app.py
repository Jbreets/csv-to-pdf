import os
import pandas as pd
from flask import Flask, request, render_template, send_file
from csvtopdf import create_pdf_from_csv  # Import your function
# from csvtopdf_2 import create_pdf_from_csv  # Import your function

app = Flask(__name__)

# Configure file upload and download folders
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return render_template('index.html', result="No file uploaded!")

        file = request.files['csv_file']

        if file.filename == '':
            return render_template('index.html', result="No selected file!")

        # Save the uploaded CSV file
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(csv_path)

        # Generate PDF filename
        pdf_filename = file.filename.replace('.csv', '.pdf')
        pdf_path = os.path.join(app.config['DOWNLOAD_FOLDER'], pdf_filename)

        # Convert CSV to PDF
        create_pdf_from_csv(csv_path, pdf_path)

        return render_template('index.html', result="PDF generated!", pdf_filename=pdf_filename)

    return render_template('index.html', result=None)

@app.route('/download/<filename>')
def download_file(filename):
    """Allows users to download the generated PDF."""
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)