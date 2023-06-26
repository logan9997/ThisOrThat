from django import template
from django.db.models import Q
from ..models import User, Post

register = template.Library()

@register.simple_tag(takes_context=True)
def add_login_status_to_context(context, request) -> str:
    '''
    Add logged_in (bool) to context 
    '''
    user_id = request.session.get('user_id', -1)
    if user_id == -1:
        context['logged_in'] = False
    else:
        context['logged_in'] = True
    return ''

@register.simple_tag
def get_username(request) -> str:
    '''
    Get the usernmame from the user_id value that is stored inside the session
    '''
    user_id = request.session.get('user_id', -1)
    user = User.objects.filter(user_id=user_id)
    if len(user) == 1:
        return user.values_list('username', flat=True)[0]
    return ''

@register.simple_tag
def get_tags_list():
    '''
    Return a list of unique tags from the database for search suggestions
    '''
    tag_strings = Post.objects.all().values_list('tags', flat=True)

    unique_tags = []
    for tag_string in tag_strings:
        if ',' in tag_string:
            tags = tag_string.split(',')
        else:
            tags = [tag_string]

        for tag in tags:
            tag = tag.strip()
            if tag not in unique_tags:
                unique_tags.append(tag)
    
    return unique_tags


@register.filter
def get(_dict:dict, params:str):
    if ',' in params:
        key = params.split(',')[0]
        return_value = params.split(',')[1]
        return _dict.get(key, return_value)
    return _dict.get(params)


@register.filter
def percentage_diff(num1, num2):
    if num1 + num2 == 0:
        return 50.0
    return round(num1 / (num1 + num2) * 100, 2)