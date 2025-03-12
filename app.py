import os
import pandas as pd
from flask import Flask, request, render_template, send_file
from csvtopdf import create_pdf_from_csv  # Import your function
from parq_export import filter_by_email  # Import your function
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
# def index():
    # if request.method == 'POST':
        # if 'csv_file' not in request.files:
            # return render_template('index.html', result="No file uploaded!")
        # file = request.files['csv_file']
        # if file.filename == '':
            # return render_template('index.html', result="No selected file!")

        # Save the uploaded CSV file
        # csv_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # file.save(csv_path)
        # Generate PDF filename
        # pdf_filename = file.filename.replace('.csv', '.pdf')
        # pdf_path = os.path.join(app.config['DOWNLOAD_FOLDER'], pdf_filename)
        # Convert CSV to PDF
        # create_pdf_from_csv(csv_path, pdf_path)
        # return render_template('index.html', result="PDF generated!", pdf_filename=pdf_filename)
    # return render_template('index.html', result=None)

@app.route('/')
def index():
    """Index Page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')



@app.route('/parq', methods=['GET', 'POST'])
def parq():
    """PARQ clean page."""
    if request.method == 'POST':
        if 'parq_file' not in request.files or 'emails' not in request.files:
            return render_template('parq-clean.html', result="Missing one or both files!")
        
        parq_file = request.files['parq_file']
        email_file = request.files['emails']

        if parq_file.filename == '' or email_file.filename == 'email_file':
            return render_template('parq-clean.html', result="No selected file!")

        parq_path = os.path.join(app.config['UPLOAD_FOLDER'], parq_file.filename)
        email_path = os.path.join(app.config['UPLOAD_FOLDER'], email_file.filename)

        parq_file.save(parq_path)
        email_file.save(email_path)

        csv_filename = "parq-cleaned-data.csv"

        filter_by_email(parq_file, email_file)

        return render_template('parq-clean.html', result="CSV generated!", csv_filename=csv_filename)

    return render_template('parq-clean.html')



@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
    """Pdf Gen page."""
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return render_template('pdf-gen.html', result="No file uploaded!")

        file = request.files['csv_file']

        if file.filename == '':
            return render_template('pdf-gen.html', result="No selected file!")

        # Save the uploaded CSV file
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(csv_path)

        # Generate PDF filename
        pdf_filename = file.filename.replace('.csv', '.pdf')
        pdf_path = os.path.join(app.config['DOWNLOAD_FOLDER'], pdf_filename)

        # Create new csv file name
        create_pdf_from_csv(csv_path, pdf_path)

        return render_template('pdf-gen.html', result="PDF generated!", pdf_filename=pdf_filename)

    # return render_template('index.html', result=None)
    return render_template('pdf-gen.html', result=None)


@app.route('/download/<filename>')
def download_file(filename):
    """Allows users to download the generated PDF."""
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)