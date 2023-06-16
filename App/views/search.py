from django.db.models import Count
from django.shortcuts import render
from ..utils import (
    insert_spaces_in_tag_string,
)
from ..config import MAX_SEARCH_SUGGESTIONS, MAX_POST_PREVIEWS_PER_PAGE
from ..forms import TagSearch
from ..sql_queries import Post 

def search(request):

    tag = '%'
    if request.method == 'GET':
        form = TagSearch(request.GET)
        if form.is_valid():
            tag = form.cleaned_data.get('tag')

    posts = Post().get_posts(where=f"WHERE tags LIKE '%{tag}%'", format=True)

    context = {
        'MAX_SEARCH_SUGGESTIONS': MAX_SEARCH_SUGGESTIONS,
        'posts': posts,
    }
    return render(request, 'App/search.html', context=context)


