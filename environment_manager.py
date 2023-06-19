import os
from dotenv import load_dotenv

class Manager():

    def __init__(self) -> None:
        self.env_path = '.env'
        load_dotenv(self.env_path)

    def get_database_credentials(self, connection:str) -> dict:
        if connection == 'settings':
            credentials = {
                'NAME': os.getenv('LOCAL_DB_NAME'),
                'USER': os.getenv('LOCAL_DB_USER'),
                'PASSWORD': os.getenv('LOCAL_DB_PASSWORD'),
                'HOST': os.getenv('LOCAL_DB_HOST'),
                'PORT': os.getenv('LOCAL_DB_PORT'),
            }
        elif connection == 'psycopg2':
            credentials = {
                'dbname': os.getenv('LOCAL_DB_NAME'),
                'user': os.getenv('LOCAL_DB_USER'),
                'password': os.getenv('LOCAL_DB_PASSWORD'),
                'host': os.getenv('LOCAL_DB_HOST'),
                'port': os.getenv('LOCAL_DB_PORT'),
            }          
        return credentials
    
    def get_items(self, *args) -> dict:
        values = {arg : os.getenv(arg) for arg in args}
        return values
    
    def get_key(self, key) -> dict:
        return os.getenv(key)
    
