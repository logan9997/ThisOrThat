from django.shortcuts import render, redirect
from ..forms import SignUp
from ..models import User
from ..utils import is_password_strong_enough, get_field_length_error

def signup(request):

    signup_error_msg = ''
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            conditons = {
                len(User.objects.filter(username=username)) == 0: 'Username Unavailable',
                password == confirm_password: 'Passwords do not match',
                is_password_strong_enough(password): 'Password does not meet requirements'
            }

            if all(conditons.keys()):
                new_user = User(username=username, password=password)
                new_user.save()
                user_id = User.objects.filter(
                    username=username, password=password
                ).values_list('user_id', flat=True)[0]

                request.session['user_id'] = user_id
                return redirect('home')
            
            signup_error_msg = conditons[False]
        else:
            signup_error_msg = get_field_length_error(str(form.errors))

    context = {
        'signup_error_msg': signup_error_msg,
    }
    return render(request, 'App/signup.html', context=context)