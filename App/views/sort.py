from django.shortcuts import redirect
from ..forms import Sort

def sort(request, sort_type):

    form = Sort(request.POST)
    if form.is_valid():
        sort_option = form.cleaned_data.get('sort_option')
        request.session[f'{sort_type}_sort_option'] = sort_option
        request.session.modified = True 

    return redirect('home')