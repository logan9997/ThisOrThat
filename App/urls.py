from django.urls import path
from .views import (
    home, post, login, create,
    search, signup, logout, vote
)

urlpatterns = [
    path(
        '', home.home, name='home'
    ),
    path(
        'post/<int:post_id>/', post.post, name='post'
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