from django.shortcuts import render
from ..config import MAX_SEARCH_SUGGESTIONS, MAX_POSTS_PER_PAGE
from ..forms import TagSearch
from ..sql_queries import Post 
from ..utils import page_boundaires
import math

def search(request):

    if 'get_params' not in request.session:
        request.session['get_params'] = {}

    #clear tag from request.session if no longer in URL
    if 'tag' in request.session['get_params'] and 'tag' not in request.GET.items():
        del request.session['get_params']['tag']
        request.session.modified = True

    tag = '%'
    if request.method == 'GET':
        form = TagSearch(request.GET)
        if form.is_valid():
            tag = form.cleaned_data.get('tag')
            request.session['get_params']['tag'] = tag
            request.session.modified = True

    posts = Post().get_posts(where=f"WHERE tags LIKE '%{tag}%'", format=True)

    pages = [i+1 for i in range(math.ceil(len(posts) / MAX_POSTS_PER_PAGE))]
    current_page = request.GET.get('page', 1)
    current_page = page_boundaires(current_page, len(pages))

    posts = posts[
        (current_page-1)*MAX_POSTS_PER_PAGE : current_page*MAX_POSTS_PER_PAGE
    ]

    context = {
        'MAX_SEARCH_SUGGESTIONS': MAX_SEARCH_SUGGESTIONS,
        'posts': posts,
        'pages': pages,
        'searched_tag': tag,
        'current_page': current_page
    }
    return render(request, 'App/search.html', context=context)


