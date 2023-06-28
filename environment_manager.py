import os
from dotenv import load_dotenv

class Manager():

    def __init__(self) -> None:
        self.env_path = '.env'
        load_dotenv(self.env_path)

    def get_database_credentials(self, connection:str) -> dict:
        '''
        Return dict of database connection credentials.
        - connection : 'settings' / 'psycopg2'
        '''
        if os.getenv('DEVELOPMENT') == 'True':
            conn_type = 'LOCAL'
        else:
            conn_type = 'HEROKU'

        if connection == 'settings':
            credentials = {
                'NAME': os.getenv(f'{conn_type}_DB_NAME'),
                'USER': os.getenv(f'{conn_type}_DB_USER'),
                'PASSWORD': os.getenv(f'{conn_type}_DB_PASSWORD'),
                'HOST': os.getenv(f'{conn_type}_DB_HOST'),
                'PORT': os.getenv(f'{conn_type}_DB_PORT'),
            }
        elif connection == 'psycopg2':
            credentials = {
                'dbname': os.getenv(f'{conn_type}_DB_NAME'),
                'user': os.getenv(f'{conn_type}_DB_USER'),
                'password': os.getenv(f'{conn_type}_DB_PASSWORD'),
                'host': os.getenv(f'{conn_type}_DB_HOST'),
                'port': os.getenv(f'{conn_type}_DB_PORT'),
            }        
       
                  
        return credentials
    
    def get_items(self, *args) -> dict:
        values = {arg : os.getenv(arg) for arg in args}
        return values
    
    def get_key(self, key) -> dict:
        return os.getenv(key)
    
