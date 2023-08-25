from os import environ

ENVIRONMENT = environ.get('ENV')
SFTP_USERNAME = environ.get('SFTP_USERNAME')
SFTP_PASSWORD = environ.get('SFTP_PASSWORD')
SFTP_HOST = environ.get('SFTP_HOST')
SFTP_PORT = environ.get('SFTP_PORT')

