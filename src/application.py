import pathlib
from os import environ
from sftputil import SFTP
from src import create_app
from src.modules.sftp_connection import SFTPConnection

create_app()
is_production_env = environ.get('ENV') == 'production'

sftp = SFTPConnection(
    hostname=environ.get('SFTP_HOST'),
    port=int(environ.get('SFTP_PORT')),
    username=environ.get('SFTP_USERNAME'),
    password=environ.get('SFTP_PASSWORD')
)

artifacts_to_download = environ.get('ARTIFACTS_TO_COPY').split(',')
for artifact in artifacts_to_download:
    remote_path = f"{environ.get('BASE_PATH_TO_COPY')}/{artifact}"
    local_path = f"{environ.get('LOCAL_PATH_TO_DOWNLOAD_BASE')}"

    if sftp.is_dir(remote_path):
        local_path = f'{local_path}/{artifact}'

    sftp.download(
        remote_path=remote_path,
        local_path=local_path)

sftp.close()
