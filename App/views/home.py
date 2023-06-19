from django.shortcuts import render
from django.db.models import Count
from ..sql_queries import Post 
from ..models import Comment
from ..config import GetSorts
from ..utils import Sort

def home(request):

    user_id = request.session.get('user_id', -1)
    posts = Post().get_posts(where=f'WHERE PO.user_id = {user_id}', format=True)
    comments = Comment.objects.filter(user_id=user_id).values().annotate(votes=Count('commentvote'))
    
    posts = Sort.sort(request, 'posts', posts)
    comments = Sort.sort(request, 'comments', comments)

    comment_sorts = GetSorts().get_comment_sorts()
    post_sorts = GetSorts().get_post_sorts()

    current_posts_sort = Sort.get_current_sort_order(request, 'posts')
    current_comments_sort = Sort.get_current_sort_order(request, 'comments')

    Sort.sort_dropdown_options(post_sorts, current_posts_sort)
    Sort.sort_dropdown_options(comment_sorts, current_comments_sort)

    context = {
        'title': 'Home',
        'posts': posts,
        'comments': comments,
        'post_sorts': post_sorts,
        'comment_sorts': comment_sorts,
        'current_posts_sort': current_posts_sort,
        'current_comments_sort': current_comments_sort,
    }
    return render(request, 'App/home.html', context=context)

