import psycopg2 
from environment_manager import Manager

class Query:

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
    
    def format(self, result:list, fields:list) -> list[dict]:
        return [
            {field: row[i] for i, field in enumerate(fields)} for row in result
        ]

    
class Post(Query):

    def __init__(self) -> None:
        super().__init__()

    def get_posts(self, **kwargs):
        '''
        Return a list of all posts, 
        ordered by : count of votes (DESC), date_posted (DESC)
        '''        
        posts = self.select(sql=f'''
            SELECT PO.*, 
            (
                SELECT count(*) 
                FROM "App_comment" CO 
                WHERE CO.post_id = PO.post_id
            ),
            (
                SELECT count(*) 
                FROM "App_postvote" VO 
                WHERE VO.post_id = PO.post_id
            )
            FROM "App_post" PO 
            LEFT OUTER JOIN "App_postvote" VO ON PO.post_id=VO.post_id
            {kwargs.get('where', '')}
            GROUP BY PO.post_id
            ORDER BY count(VO.*) DESC, date_posted DESC
        '''
        )

        fields = [
            'post_id', 'description_one', 'description_two', 'image_one', 
            'image_two', 'status', 'date_posted', 'tags', 'user_id', 'title',
            'main_description', 'comments', 'votes'
        ]

        print(kwargs.get('format', False), kwargs)
        if kwargs.get('format', False):
            posts = self.format(posts, fields)
        print(posts)
        return posts

