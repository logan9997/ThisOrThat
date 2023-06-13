from django.shortcuts import redirect
from ..models import Vote, Post
from ..forms import VoteOption

def vote(request, post_id:int):
    user_id = request.session.get('user_id', -1)

    if request.method == 'POST':
        form = VoteOption(request.POST)

        if len(Post.objects.filter(user_id=user_id, post_id=post_id)) != 0:
            request.session['vote_error_msg'] = "You can't vote on your own post."
            request.session.modified = True
            return redirect('post', post_id=post_id)
    
        if form.is_valid():
            option = form.cleaned_data.get('vote_option')

            current_vote = Vote.objects.filter(
                user_id=user_id, post_id=post_id
            )

            #deselect vote if same option selected as the previously selected option 
            if option in current_vote.values_list('option', flat=True):
                current_vote.delete()
                return redirect('post', post_id=post_id)
            
            if len(current_vote) != 0:
                current_vote.delete()

            new_vote = Vote(
                post_id=post_id,
                user_id=user_id,
                option=option
            )
            new_vote.save()

    return redirect('post', post_id=post_id)