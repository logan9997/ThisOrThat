from django import template
from ..models import User

register = template.Library()

@register.simple_tag(takes_context=True)
def add_login_status_to_context(context, request):
    user_id = request.session.get('user_id', -1)
    if user_id == -1:
        context['logged_in'] = False
    else:
        context['logged_in'] = True
    return ''

@register.simple_tag
def get_username(request):
    user_id = request.session.get('user_id', -1)
    user = User.objects.filter(user_id=user_id)
    if len(user) == 1:
        return user.values_list('username', flat=True)[0]
    return ''