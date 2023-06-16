from django.urls import path
from .views import (
    home, post, login, create,
    search, signup, logout, vote,
    comment
)

urlpatterns = [
    path(
        '', home.home, name='home'
    ),
    path(
        'post/<int:post_id>/', post.post, name='post'
    ),
    path(
        'comment/<int:post_id>/', comment.comment, name='comment'
    ),
    path(
        'comment_vote/<int:comment_id>/<int:post_id>/', comment.comment_vote,
        name='comment_vote'
    ),
    path(
        'delete_comment/<int:comment_id>/<int:post_id>/', 
        comment.delete_comment, name='delete_comment'
    ),
    path(
        'login/', login.login, name='login'
    ),
    path(
        'signup/', signup.signup, name='signup'
    ),
    path(
        'logout/', logout.logout, name='logout'
    ),
    path(
        'create/', create.create, name='create'
    ),
    path(
        'search/', search.search, name='search'
    ),
    path(
        'vote/<int:post_id>/', vote.vote, name='vote'
    ),
]