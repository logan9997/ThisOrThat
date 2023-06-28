#USER
MAX_USERNAME_LENGTH = 16
MAX_EMAIL_LENGTH = 60
MAX_PASSWORD_LENGTH = 24

#POST
MAX_MAIN_DESCRIPTION_LENTGH = 1200
MAX_DESCRIPTION_LENGTH = 500
MAX_TAGS_LENGTH = 120
MAX_STATUS_LENGTH = 6
MAX_TITLE_LENGTH = 50
MAX_BUTTON_LABEL_LENGTH = 25

#COMMENT
MAX_COMMENT_LENGTH = 1000

#PASSWORD
MIN_PASSWORD_LENGTH = 8
MIN_UPPERCASE_CHARS = 1
MIN_SPECIAL_CHARS = 1

PASSWORD_REQUIREMENTS = [
    'Password : ',
    f'Min ({MIN_PASSWORD_LENGTH}) Characters',
    f'Min ({MIN_SPECIAL_CHARS}) Special Characters', 
    f'Min ({MIN_UPPERCASE_CHARS}) Uppercase Characters'
]

#GENERAL
MAX_SEARCH_SUGGESTIONS = 12
MAX_POST_PREVIEWS_PER_PAGE = 20
MAX_TAGS = 5
# VALID_IMAGE_EXTENSIONS = ('.jpg', '.png', 'jpeg', 'jfif')
MAX_TAG_LENGTH = MAX_TAGS_LENGTH // MAX_TAGS
MAX_POSTS_PER_PAGE = 12

#SORTS
class GetSorts:
    COMMENT_SORTS = [
            {'text':'Votes high to low', 'value':'votes-True'},
            {'text':'Votes low to high', 'value':'votes-False'},
            {'text':'Newest', 'value':'date_posted-True'},
            {'text':'Oldest', 'value':'date_posted-False'},
    ]

    POST_SORTS = [
            {'text':'Comments high to low', 'value':'comments-True'},
            {'text':'Comments low to high', 'value':'comments-False'},
    ]
    def get_comment_sorts(self):
        return self.COMMENT_SORTS

    def get_post_sorts(self):
        empty_post_sorts = []
        empty_post_sorts.extend(self.POST_SORTS)
        empty_post_sorts.extend(self.COMMENT_SORTS)
        return empty_post_sorts