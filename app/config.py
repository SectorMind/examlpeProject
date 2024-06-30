# app/config.py
import secrets

import dotenv
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

env = dotenv.dotenv_values()

DBMS = env["DBMS"]
USER_NAME = env["USER_NAME"]
PASSWORD = env["PASSWORD"]
HOST = env["HOST"]
PORT = env["PORT"]
DATABASE_NAME = env["DATABASE_NAME"]
# DRIVER = env["DRIVER"]
DRIVER = env.get('DRIVER')
TOKEN = env.get('TOKEN')

SECRET_KEY = env.get('SECRET_KEY')
ALGORITHM = env.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

DATABASE_URL = f"{DBMS}{f'+{DRIVER}' if DRIVER else ''}://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}"

if __name__ == '__main__':
    print(secrets.token_hex(20))
