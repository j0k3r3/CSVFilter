from flask import render_template, request, redirect, url_for, flash, current_app as app, send_file
import os
import pandas as pd
from io import BytesIO
from .utils import allowed_file

@app.route('/')
def index():
    
    # Delete all CSV files in the upload folder
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.csv'):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # List all CSV files in the upload folder (should be empty after deletion)
    #csv_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.csv')]
    
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    flash(f"Route: {app.config['UPLOAD_FOLDER']}")
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash('File successfully uploaded')
        return redirect(url_for('filter_data', filename=filename))
    else:
        flash('Invalid file format')
        return redirect(request.url)

@app.route('/filter/<filename>', methods=['GET', 'POST'])
def filter_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
    filtered_df = None

    if request.method == 'POST':
        column = request.form.get('column')
        value = request.form.get('value')
        column2 = request.form.get('column2')
        value2 = request.form.get('value2')
        order = request.form.get('order')
        
        if column and value and order:
            
            # Perform data filtering and ordering (example with pandas DataFrame)
            # Assuming 'data' is your DataFrame or data source
            filtered_df = df[df[column].astype(str).str.contains(value, na=False)]

            #Second filter
            if column2 and value2:
                filtered_df = filtered_df[filtered_df[column2].astype(str).str.contains(value2, na=False)].sort_values(by=order)

            # Convert filtered_data to HTML table format for rendering
            tables_html = [filtered_df.to_html(classes='table table-striped')]
            
            return render_template('filter.html', columns=df.columns, tables=tables_html, titles=filtered_df.columns.values, filename=filename, filtered=True)

    return render_template('filter.html', columns=df.columns, filename=filename, filtered=False)

@app.route('/download/<filename>', methods=['POST'])
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
    column = request.form.get('column')
    value = request.form.get('value')
    column2 = request.form.get('column2')
    value2 = request.form.get('value2')
    order = request.form.get('order')
    
    filtered_df = df[df[column].astype(str).str.contains(value, na=False)]
    if column2 and value2:
        filtered_df = filtered_df[filtered_df[column2].astype(str).str.contains(value2, na=False)].sort_values(by=order)


    output = BytesIO()
    filtered_df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, mimetype='text/csv', download_name='filtered_data.csv', as_attachment=True)