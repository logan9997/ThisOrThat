from django.shortcuts import render
from ..models import Post, Vote
from ..forms import VoteOption
from ..utils import (
    is_image_file_extension_valid, insert_spaces_in_tag_string,
)

def post(request, post_id):

    user_id = request.session.get('user_id', -1)

    #find row where user has voted on this post if exists
    current_vote = Vote.objects.filter(
        user_id=user_id, post_id=post_id
    )
    
    if len(current_vote) != 0:
        #get the option which the user voted for
        current_vote = current_vote.values_list(
            'option', flat=True
        )[0]

    post = Post.objects.filter(post_id=post_id).values()[0]

    # possibly reduntant with js function adding spaces?
    post['tags'] = insert_spaces_in_tag_string(post['tags'])
    for image in ['image_one', 'image_two']:
        if is_image_file_extension_valid(post[image]):
            post[image] = '../../media/' + post[image]
        else:
            post[image] = '../../media/images/empty_post_image.png'

    context = {
        'title': 'Post',
        'post': post,
        'current_vote': current_vote,
        'vote_error_msg': request.session.get('vote_error_msg')
    }

    if 'vote_error_msg' in request.session:
        del request.session['vote_error_msg']
        
    return render(request, 'App/post.html', context=context)