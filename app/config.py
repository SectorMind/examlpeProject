import os
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
DATABASE_URL = f"{DBMS}{f'+{DRIVER}' if DRIVER else ''}://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}"

if __name__ == '__main__':
    pass
