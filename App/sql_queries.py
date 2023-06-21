import psycopg2 
from environment_manager import Manager

class Query:

    def __init__(self) -> None:
        self.database_credentials = Manager().get_database_credentials('psycopg2')
        self.conn = psycopg2.connect(**self.database_credentials)
        self.cursor = self.conn.cursor()

    def format_result(func) -> list[dict]:
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)

            if kwargs.get('format', False) and kwargs.get('fields', False):
                result = [
                    {field: row[i] for i, field in enumerate(kwargs['fields'])} 
                    for row in result
                ]
            return result
        return inner

    @format_result
    def select(self, sql, **kwargs):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if kwargs.get('flat'):
            return [row[0] for row in result]
        return result
    
    
class Post(Query):

    def test(self):
        sql = 'select * from "App_user"'
        result = self.select(sql, format=True)
        return result

    def get_posts(self, **kwargs):
        '''
        Return a list of all posts, 
        ordered by : count of votes (DESC), date_posted (DESC)
        '''        
        sql=f'''
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
            ),
            (
                SELECT username
                FROM "App_user" US
                WHERE US.user_id = PO.user_id
            )
            FROM "App_post" PO
            LEFT OUTER JOIN "App_postvote" VO ON PO.post_id=VO.post_id
            LEFT OUTER JOIN "App_comment" CO ON PO.post_id=CO.post_id
            {kwargs.get('where', '')}
            GROUP BY PO.post_id
            ORDER BY (COUNT(VO.*) + COUNT(CO.*)) DESC, date_posted DESC
        '''

        fields = [
            'post_id', 'description_one', 'description_two', 'image_one', 
            'image_two', 'status', 'date_posted', 'tags', 'user_id', 'title',
            'main_description', 'comments', 'votes', 'username'
        ]

        return self.select(sql, format=True, fields=fields)

    def get_comments(self, user_id, post_id):
        sql=f'''
            SELECT comment, CO.comment_id, date_posted, US.user_id, username, (
                SELECT option 
                FROM "App_commentvote" CV 
                WHERE user_id = {user_id}
                    AND CV.comment_id = CO.comment_id
            ) AS "option", (
                (
                    SELECT COUNT(*) 
                    FROM "App_commentvote" CV 
                    WHERE option='Up' 
                        AND CV.comment_id = CO.comment_id
                ) - (
                    SELECT COUNT(*) 
                    FROM "App_commentvote" CV 
                    WHERE option='Down' 
                    AND CV.comment_id = CO.comment_id
                )
            ) AS "votes"
            FROM "App_comment" CO, "App_user" US
            WHERE CO.user_id = US.user_id
                AND post_id = {post_id}
            ORDER BY votes DESC
        '''
        fields = [
            'comment', 'comment_id', 'date_posted', 'user_id', 
            'username', 'current_vote', 'votes'
        ]

        return self.select(sql, format=True, fields=fields)

class Home(Query):
    
    def get_comments(self, user_id):
        sql=f'''
            SELECT CO.*, title, (
                (
                    SELECT COUNT(*) 
                    FROM "App_commentvote" CV 
                    WHERE option='Up' 
                        AND CV.comment_id = CO.comment_id
                ) - (
                    SELECT COUNT(*) 
                    FROM "App_commentvote" CV 
                    WHERE option='Down' 
                    AND CV.comment_id = CO.comment_id
                )
            ) AS "votes"
            FROM "App_comment" CO, "App_user" US, "App_post" PO
            WHERE CO.user_id = {user_id}
                AND CO.post_id = PO.post_id
                AND PO.user_id = US.user_id
            ORDER BY votes DESC           
        '''

        fields = [
            'comment_id', 'comment', 'date_posted', 'post_id', 
            'user_id', 'post_title', 'votes'
        ]

        return self.select(sql, format=True, fields=fields)


        
        