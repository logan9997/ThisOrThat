from django.shortcuts import redirect

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')