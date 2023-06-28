from django.shortcuts import redirect
from ..forms import Page

def pages(request):
    page = 1
    if request.method == 'GET':
        form = Page(request.GET)
        if form.is_valid():
            page = form.cleaned_data.get('page')
    
    if 'get_params' not in request.session:
        request.session['get_params'] = {}

    #add query string to end of URL
    response = redirect('search')
    query_string = f'?page={page}'
    tag = request.session['get_params'].get('tag', False)
    if tag:
        query_string += f'&tag={tag}'

    response['location'] += query_string
    return response