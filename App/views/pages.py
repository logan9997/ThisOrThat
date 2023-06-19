from django.shortcuts import redirect
from ..forms import Page

def pages(request):
    if request.method == 'GET':
        form = Page(request.GET)
        if form.is_valid():
            page = form.cleaned_data.get('page')
    
    #add query string to end of URL
    response = redirect('search')
    query_string = f'?page={page}'
    print(request.session['get_params'].get('tag', False))
    if tag := request.session['get_params'].get('tag', False):
        print('if met')
        query_string += f'&tag={tag}'

    response['location'] += query_string
    return response