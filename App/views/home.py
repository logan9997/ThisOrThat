from django.shortcuts import render
from ..sql_queries import Post, Home
from ..config import GetSorts
from ..utils import Sort
from ..models import Post as PostModel
from random import choice

def home(request):

    user_id = request.session.get('user_id', -1)
    posts = Post().get_posts(where=f'WHERE PO.user_id = {user_id}')
    comments = Home().get_comments(user_id)

    posts = Sort.sort(request, 'posts', posts)
    comments = Sort.sort(request, 'comments', comments)

    comment_sorts = GetSorts().get_comment_sorts()
    post_sorts = GetSorts().get_post_sorts()

    current_posts_sort = Sort.get_current_sort_order(request, 'posts')
    current_comments_sort = Sort.get_current_sort_order(request, 'comments')

    Sort.sort_dropdown_options(post_sorts, current_posts_sort)
    Sort.sort_dropdown_options(comment_sorts, current_comments_sort)

    post_ids = PostModel.objects.all().values_list('post_id', flat=True)
    random_post_id = choice(post_ids)

    context = {
        'title': 'Home',
        'posts': posts,
        'comments': comments,
        'post_sorts': post_sorts,
        'comment_sorts': comment_sorts,
        'current_posts_sort': current_posts_sort,
        'current_comments_sort': current_comments_sort,
        'random_post_id': random_post_id
    }
    return render(request, 'App/home.html', context=context)

