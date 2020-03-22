import os
from config import Config
from flask import request,jsonify
from CILogParser import CILogParser
from werkzeug.utils import secure_filename


def validate_file(filename):
    """
    This function checks for file extensions
    :param filename: filename uploaded
    :return: True if its one of specified extensions in config file
    """
    if filename.split('.')[-1].lower() in Config.ALLOWED_EXTENSIONS:
        return True


def post_file():
    """
    Recieves the uploaded file and parses the file based on rules specified in the custom CI LogParser package
    :return: Parsed Dictionary of the selected log prints
    """
    file = request.files['inputfile']
    filename = secure_filename(file.filename)
    if validate_file(filename):
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        with open(os.path.join(Config.UPLOAD_FOLDER, filename)) as f:
            myapp = CILogParser.LogParser()
            parsed_gen = list(myapp.generate_dict(f))
        return jsonify({"result": parsed_gen},)
    else:
        return "Invalid file extension"



