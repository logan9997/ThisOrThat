from django.shortcuts import render, redirect
from ..forms import Login
from ..models import User
from ..config import USERNAME_LENGTH, PASSWORD_LENGTH

def login(request):

    login_error_msg = ''

    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username:str = form.cleaned_data.get('username')
            password:str = form.cleaned_data.get('password')

            #__iexact ignores case
            user = User.objects.filter(username__iexact=username, password=password)

            if len(user) == 1:
                user_id = user.values_list('user_id', flat=True)[0]
                request.session['user_id'] = user_id
                return redirect('home')
            
            login_error_msg = 'Username and Password do not match'
        else:
            login_error_msg = get_field_length_error(str(form.errors))

    context = {
        'title': 'Login',
        'login_error_msg':login_error_msg,
    }
    return render(request, 'App/login.html', context=context)


def get_field_length_error(error:str) -> str:
    '''
    Return which field is has too many characters from form.errors
    '''
    if str(USERNAME_LENGTH) in error:
        return f'Username is too long ({USERNAME_LENGTH} Chars)'
    
    if str(PASSWORD_LENGTH) in error:
        return f'Password is too long ({PASSWORD_LENGTH} Chars)'
    return ''