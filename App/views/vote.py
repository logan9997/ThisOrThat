from django.shortcuts import redirect
from ..models import PostVote
from ..forms import VoteOption
from ..utils import Vote

def vote(request, post_id:int):
    user_id = request.session.get('user_id', -1)

    if user_id == -1:
        request.session['vote_error_msg'] = "You must be logged in to vote."
        request.session.modified = True
        return redirect('post', post_id=post_id)       

    if request.method == 'POST':
        form = VoteOption(request.POST)

        if form.is_valid():
            Vote.vote_handler(
                request, 
                form, 
                post_id, 
                user_id, 
                PostVote
            )

    return redirect('post', post_id=post_id)