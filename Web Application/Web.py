import subprocess
import os
import logging 
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify, send_file
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from logging.handlers import RotatingFileHandler  # Import the necessary handler

# ... Other Flask configuration ...

# Configure logging
if not app.debug:  # Only enable logging in non-debug mode
    log_filename = 'log_file.log'  # Specify the log file name
    log_handler = RotatingFileHandler(log_filename, maxBytes=1024*1024, backupCount=10)  # Configure the file handler
    log_handler.setLevel(logging.INFO)  # Set the log level (e.g., INFO)
    app.logger.addHandler(log_handler)  # Add the file handler to the Flask logger


app = Flask(__name__)

# Azure Storage Account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=tshfhjabishekasrcache;AccountKey=inz+3kkO6JnpA6DyO+fWa/N72Qc60ijYntyU+wxeWZjLS4u7uNdJrf6h47lErtirJixu8PjVa82g+AStK2XcWQ==;EndpointSuffix=core.windows.net"

# Blob Container name
container_name = "asr-254ad3cd-421e-9b77-0ccfb919371a"

# Specify the path where uploaded files will be stored
UPLOAD_FOLDER = 'C:/Users/Abishek/Documents/JoJoGAN/input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the environment variable
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/latest_output_image')
def latest_output_image():
    # Initialize the BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # List all blobs in the container
    blob_list = container_client.list_blobs()

    # Sort the blobs by modification time to get the latest one
    latest_blob = max(blob_list, key=lambda x: x['last_modified'])

    # Get the URL of the latest blob
    latest_blob_url = container_client.url + "/" + latest_blob.name

    return latest_blob_url


@app.route('/run_script', methods=['POST'])
def run_script():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    file = request.files['file']

    # Check if the file has a filename
    if file.filename == '':
        return jsonify({"message": "No selected file"})

    if file:
        # Generate a unique filename based on the current datetime
        current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = file.filename #current_datetime + '_' + file.filename

        # Save the uploaded file to the specified folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Now, you can use 'filename' as the path to the uploaded file
        input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Specify the path to your script
        os.chdir('C:/Users/Abishek/Documents/JoJoGAN')

        # Get the base filename without the extension
        base_filename, file_extension = os.path.splitext(os.path.basename(input_file))

        # Get the current datetime in the desired format (e.g., YYYYMMDD_HHMMSS)
        current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Combine the base filename, datetime, and original file extension
        new_filename = f'{base_filename}_{current_datetime}{file_extension}'

        # Create the full path for the new file with forward slashes
        new_filepath = os.path.join(os.path.dirname(input_file), new_filename)

        new_filepath_updated = new_filepath.replace('\\', '/')

        # Rename the input file with the new filename
        os.rename(input_file, new_filepath_updated)

        # Replace 'azureml_py38' with the name of your Conda environment
        conda_env = 'py38_default'

        # Specify the full path to the Conda executable within the environment
        conda_executable = 'conda'

        # Activate the Conda environment by creating a new shell process
        activate_command = f'{conda_executable} activate {conda_env}'
        subprocess.run(activate_command, shell=True)

        # Specify the name of your Python script (e.g., 'StyleDisney.py')
        script_name = 'C:/Users/Abishek/Documents/JoJoGAN/StyleDisney.py'

        # Combine the command to activate the Conda environment and run the script with the new filename
        #full_command = f'python {script_name} -f {new_filepath_updated}'
        full_command = f'conda run -n {conda_env} python {script_name} -f {new_filepath_updated}'

        # Run the combined command
        subprocess.run(full_command, shell=True)

        # Specify the directory path where the files are stored
        out_directory_path = r'C:/Users/Abishek\Documents/JoJoGAN/output'

        # Run a command to list the files in the directory
        command = f'dir /b /o-d "{out_directory_path}"'  # This command lists files in descending order by date
        output = subprocess.check_output(command, shell=True, text=True)

        # Split the output into lines
        lines = output.strip().split('\n')

        if lines:
            # Get the first line, which is the latest file
            latest_file = lines[0]

            # Construct the full path to the latest file
            latest_image_path = os.path.join(out_directory_path, latest_file)

            return jsonify({"message": "Script executed successfully", "latest_image_path": latest_image_path})
        else:
            return jsonify({"message":"No files found in the directory"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

