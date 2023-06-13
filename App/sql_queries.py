import psycopg2 
from environment_manager import Manager

class Query():

    def __init__(self) -> None:
        self.database_credentials = Manager().get_database_credentials('psycopg2')
        self.conn = psycopg2.connect(**self.database_credentials)
        self.cursor = self.conn.cursor()

    def select(self, sql, **kwargs):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if kwargs.get('flat'):
            return [row[0] for row in result]
        return result
    
