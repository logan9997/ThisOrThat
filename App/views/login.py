from django.shortcuts import render, redirect
from ..forms import Login
from ..models import User
from ..utils import get_field_length_error, FormRestrictions

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
        'input_restrictions': FormRestrictions().login_signup()
    }
    return render(request, 'App/login.html', context=context)


