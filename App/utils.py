from password_strength import PasswordPolicy
from django.db.models import Model
from django.forms import Form
from .models import Comment, Post
from django.shortcuts import redirect
from .config import (
    VALID_IMAGE_EXTENSIONS, MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH, MIN_SPECIAL_CHARS, MIN_UPPERCASE_CHARS,    
    MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH, MAX_TAG_LENGTH, 
    MAX_MAIN_DESCRIPTION_LENTGH
)

class FormRestrictions:

    def create_post() -> dict:
        restrictions = {
            'title_max_length': MAX_TITLE_LENGTH,
            'main_description_max_length': MAX_MAIN_DESCRIPTION_LENTGH,
            'description_max_length': MAX_DESCRIPTION_LENGTH,
            'tag_max_length': MAX_TAG_LENGTH + 1 # account for comma at end of each tag
        }
        return restrictions
    
    def login_signup():
        restrictions = {
            'username_max_length': MAX_USERNAME_LENGTH,
            'password_max_length': MAX_PASSWORD_LENGTH
        }
        return restrictions


class Vote:

    def vote_handler(request, form:Form, post_id:int, user_id:int, model:Model):
        '''
        Handle voting for votes on comments or posts.
        - form = VoteOption / CommentVote
        - post_id = id of post, used to redirect back to the current post 
        - user_id = id of currently logged in user, for filtering models
        - model = PostVote / CommentVote
        '''
        #can't vote if not logged in
        if user_id == -1:
            request.session['vote_error_msg'] = 'You must be logged in to vote'
            request.session.modified = True
            return redirect('post', post_id=post_id)
        
        #set kwargs_post_id (the pk for the model passed as the last parameter)
        #set master_model (model to check if the user is voting on their own post)
        if 'PostVote' in model.__name__:
            kwargs_post_id = {'post_id': post_id}
            master_model = Post
        elif 'CommentVote' in model.__name__: 
            kwargs_post_id = {'comment_id': post_id}
            master_model = Comment

        #check if the user votes on their own post
        if len(master_model.objects.filter(user_id=user_id, **kwargs_post_id)) != 0:
            request.session['vote_error_msg'] = f"You can't vote on your own {master_model.__name__}"
            request.session.modified = True
            return redirect('post', post_id=post_id) 

        current_vote = model.objects.filter(
            user_id=user_id, **kwargs_post_id
        )

        vote_option = form.cleaned_data.get('vote_option')
        #deselect vote if same option selected as the previously selected option 
        if vote_option in current_vote.values_list('vote_option', flat=True):
            current_vote.delete()
            return redirect('post', post_id=post_id)
        
        #delete previous vote
        if len(current_vote) != 0:
            current_vote.delete()

        #save new vote
        new_vote = model(
            user_id=user_id,
            vote_option=vote_option,   
            **kwargs_post_id         
        )
        new_vote.save()
    

class Sort:

    def sort(request, post_type:str, iterable:list) -> tuple[list, str]:
        '''
        Sort comments or posts based on the sort field and order set in 
        request.session after sort.py is called.
        - post_type = 'comments' / 'posts'
        - iterable = comments / posts
        '''
        if current_sort := request.session.get(f'{post_type}_sort_option'):
            sort_field:str = current_sort.split('-')[0]
            sort_order:bool = current_sort.split('-')[1] == 'True'
            iterable = sorted(iterable, key=lambda x: x[sort_field], reverse=sort_order)
        return iterable

    def get_current_sort_order(request, post_type) -> str:
        '''
        Return the current sort order for either posts or comments
        '''
        return request.session.get(f'{post_type}_sort_option')

    def sort_dropdown_options(options:list, selected_option:str) -> None:
        '''
        Swap element 0 with element at the index of selected_option in a list
        of dropdown options
        '''
        selected_option_index = next(
            (i for i, _dict in enumerate(options) if _dict['value'] == selected_option)
        , False)

        if not selected_option_index:
            return

        options[0], options[selected_option_index] = options[selected_option_index], options[0]
    

def page_boundaires(page:int, max_pages:int) -> int:
    try:
        page = int(page)
    except:
        return 1

    if page < 1:
        return 1
    if page > max_pages:
        return max_pages
    return page


def is_image_file_extension_valid(image_path:str) -> bool:
    '''
    Check if the an images contains an any valid file extension.
    Valid image extensions saved in config.py
    '''
    if image_path == None:
        return False

    for extension in VALID_IMAGE_EXTENSIONS:
        print(image_path[-len(extension):].lower(), extension)
        if image_path[-len(extension):].lower() == extension:
            return True
    return False


def get_field_length_error(error:str) -> str:
    '''
    Return which field is has too many characters from form.errors
    '''
    if type(error) != str:
        error = str(error)

    if str(MAX_USERNAME_LENGTH) in error:
        return f'Username is too long ({MAX_USERNAME_LENGTH} Chars)'
    
    if str(MAX_PASSWORD_LENGTH) in error:
        return f'Password is too long ({MAX_PASSWORD_LENGTH} Chars)'
    return ''


def is_password_strong_enough(password:str) -> bool:
    '''
    Returns True is password passes all requirements,
    otherwise returns False
    '''
    policy = PasswordPolicy.from_names(
        length=MIN_PASSWORD_LENGTH,
        uppercase=MIN_UPPERCASE_CHARS,
        special=MIN_SPECIAL_CHARS
    )

    test_result = policy.test(password)

    if test_result == []:
        return True
    return False

#POSSIBLY REDUNDANT

def insert_spaces_in_tag_string(tag_string:str) -> str:
    '''
    Adds spaces after each comman in tag_string for readability on the UI
    '''
    tag_string = ''.join([
        char if char != ',' else f'{char} ' for char in tag_string
    ])
    return tag_string