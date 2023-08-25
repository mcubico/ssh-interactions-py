import errno
import logging
import os.path
import time

from paramiko.sftp_client import SFTPClient
from paramiko.transport import Transport
from stat import S_ISDIR, S_ISREG
from sftputil import SFTP


class SFTPConnection:
    _username: str
    _password: str
    _port: int
    _hostname: str
    _connection: SFTPClient | None

    def __init__(self, hostname: str, username: str, password: str, port: int = 22):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password

        self.open_connection()

    def open_connection(self):
        transport = Transport(sock=(self._hostname, self._port))
        transport.connect(username=self._username, password=self._password)
        self._connection = SFTPClient.from_transport(transport)
        logging.info('SFTP connection open')

    def download(self, remote_path: str, local_path: str, retry: int = 5):
        try:
            if not self._file_exists(remote_path):
                raise FileNotFoundError(f"'{remote_path}' not found on '{self._hostname}'")

            if not os.path.exists(local_path):
                os.makedirs(local_path)

            if self._is_dir(remote_path):
                self._download_dir(remote_path, local_path)
            else:
                self._download_file(remote_path, local_path, retry)
        except Exception as ex:
            raise ex

    def upload(self, local_path: str, remote_path: str):
        self._connection.put(localpath=local_path,
                             remotepath=remote_path,
                             callback=self.uploading_info,
                             confirm=True)

    @staticmethod
    def uploading_info(uploaded_file_size, total_file_size):
        message = 'uploaded_file_size : {} total_file_size : {}'.format(uploaded_file_size, total_file_size)
        print(message)

    def _file_exists(self, remote_path):
        try:
            self._connection.stat(remote_path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True

    def _is_dir(self, path):
        try:
            attr = self._connection.stat(str(path))
            return S_ISDIR(attr.st_mode)
        except FileNotFoundError:
            return False

    def _is_file(self, path):
        try:
            attr = self._connection.stat(str(path))
            return S_ISREG(attr.st_mode)
        except FileNotFoundError:
            return False

    def _download_dir(self, remote_path: str, local_path: str):
        sftp = SFTP(
            hostname=self._hostname,
            port=self._port,
            username=self._username,
            password=self._password
        )

        sftp.sync_pull(
            remote_path=remote_path,
            local_directory=local_path
        )

    def _download_file(self, remote_path: str, local_path: str, retry: int = 5):
        if self._file_exists(remote_path) or retry == 0:
            self._connection.get(remote_path, local_path, callback=None)
            logging.info(f'Downloaded {remote_path}')
        elif retry > 0:
            time.sleep(5)
            logging.info(f'Try to download: {retry}')
            retry = retry - 1
            self.download(remote_path, local_path, retry=retry)

    def close(self):
        self._connection.close()
        logging.debug('SFTP connection closed')