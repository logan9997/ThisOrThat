from django.db.models import Count
from django.shortcuts import render
from ..utils import (
    insert_spaces_in_tag_string,
)
from ..config import MAX_SEARCH_SUGGESTIONS, MAX_POST_PREVIEWS_PER_PAGE
from ..forms import TagSearch
from ..models import Post
from ..sql_queries import Query

def search(request):
    user_id = request.session.get('user_id', -1)

    post_ids = Query().select(sql=f'''
        SELECT PO.post_id
        FROM "App_post" PO
        LEFT OUTER JOIN "App_vote" V ON PO.post_id=v.post_id
        GROUP BY PO.post_id
        ORDER BY count(V.*) DESC, date_posted DESC
    ''', flat=True)

    print(post_ids)
    posts = Post.objects.filter(post_id__in=post_ids)

    if request.method == 'GET':
        form = TagSearch(request.GET)
        if form.is_valid():
            tag = form.cleaned_data.get('tag')

            posts = Post.objects.filter(tags__icontains=tag)

    posts = posts.values(
        'title', 'date_posted', 'tags', 'post_id', 'user__username'
    ).annotate(votes=Count('vote')).order_by('-votes')[:MAX_POST_PREVIEWS_PER_PAGE]

    for post in posts:
        # possibly reduntant with js function adding spaces?
        post['tags'] = insert_spaces_in_tag_string(post['tags'])

    context = {
        'MAX_SEARCH_SUGGESTIONS': MAX_SEARCH_SUGGESTIONS,
        'posts': posts,
    }
    return render(request, 'App/search.html', context=context)


