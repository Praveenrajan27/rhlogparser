import os


class Config:
    #App level Configs
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024 #Allows max of 8Mb


    #File Configs
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
    ALLOWED_EXTENSIONS = {'log', 'txt'}

    #regex config
    INCLUDE_ALL_TESTCASE = True  # Flag to include testcases entries


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    DEBUG = False
    TESTING = True