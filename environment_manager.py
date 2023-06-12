import os
from dotenv import load_dotenv

class Manager():

    def __init__(self) -> None:
        self.env_path = '.env'
        load_dotenv(self.env_path)

    def get_database_credentials(self):
        credentials = {
            'NAME': os.getenv('LOCAL_DB_NAME'),
            'USER': os.getenv('LOCAL_DB_USER'),
            'PASSWORD': os.getenv('LOCAL_DB_PASSWORD'),
            'HOST': os.getenv('LOCAL_DB_HOST'),
            'PORT': os.getenv('LOCAL_DB_PORT'),
        }
        return credentials
    
    def get_development(self):
        return os.getenv('DEVELOPMENT')