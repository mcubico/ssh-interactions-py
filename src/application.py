import pathlib
from os import environ
from sftputil import SFTP
from src import create_app
from src.modules.sftp_connection import SFTPConnection

create_app()
is_production_env = environ.get('ENV') == 'production'
print(f'app: is production: {is_production_env}')
remote_path = '/home/p0431u9d2x4l/public_html/test.academiastart.bitcubico.com'
download_path = 'downloads'

sftp = SFTPConnection(
    hostname=environ.get('SFTP_HOST'),
    port=int(environ.get('SFTP_PORT')),
    username=environ.get('SFTP_USERNAME'),
    password=environ.get('SFTP_PASSWORD')
)

sftp.download(remote_path=remote_path, local_path=download_path)
