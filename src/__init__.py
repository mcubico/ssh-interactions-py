import os
import logging

from dotenv import load_dotenv


def create_app():

    # the path to your .env file (or any other file of environment variables you want to load)
    load_dotenv('.env')
    is_production_env = os.environ.get('ENV') == 'production'

    if is_production_env:
        logging.basicConfig(filename='logs.log')

    if __name__ == '__main__':
        print('Debug mode')
