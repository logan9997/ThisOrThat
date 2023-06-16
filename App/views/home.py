from django.shortcuts import render
from ..sql_queries import Post 
from ..models import Comment
from django.db.models import F

def home(request):

    user_id = request.session.get('user_id', -1)
    posts = Post().get_posts(where=f'WHERE PO.user_id = {user_id}', format=True)
    comments = Comment.objects.filter(user_id=user_id).values()#.annotate(post_id=F('post__post_id'))

    context = {
        'title': 'Home',
        'posts': posts,
        'comments': comments
    }
    return render(request, 'App/home.html', context=context)