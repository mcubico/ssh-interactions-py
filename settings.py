from os import environ

ENVIRONMENT = environ.get('ENV')
SFTP_USERNAME = environ.get('SFTP_USERNAME')
SFTP_PASSWORD = environ.get('SFTP_PASSWORD')
SFTP_HOST = environ.get('SFTP_HOST')
SFTP_PORT = environ.get('SFTP_PORT')
BASE_PATH_TO_COPY = environ.get('BASE_PATH_TO_COPY')
ARTIFACTS_TO_COPY = environ.get('ARTIFACTS_TO_COPY')
LOCAL_PATH_TO_DOWNLOAD_BASE = environ.get('LOCAL_PATH_TO_DOWNLOAD_BASE')
