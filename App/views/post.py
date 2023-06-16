from django.shortcuts import render
from django.db.models import F
from ..models import Post, PostVote
from ..utils import (
    is_image_file_extension_valid
)
from ..sql_queries import Query

def post(request, post_id):

    user_id = request.session.get('user_id', -1)

    #find row where user has voted on this post if exists
    current_vote = PostVote.objects.filter(
        user_id=user_id, post_id=post_id
    )
    
    if len(current_vote) != 0:
        #get the option which the user voted for
        current_vote = current_vote.values_list(
            'option', flat=True
        )[0]

    post = Post.objects.filter(post_id=post_id).values().annotate(
        username=F('user__username')
    )[0]

    # possibly reduntant with js function adding spaces?
    for image in ['image_one', 'image_two']:
        if is_image_file_extension_valid(post[image]):
            post[image] = '../../media/' + post[image]
        else:
            post[image] = '../../media/images/empty_post_image.png'

    comments = Query().select(sql=f'''
        SELECT comment, CO.comment_id, date_posted, US.user_id, username, (
            SELECT option 
            FROM "App_commentvote" CV 
            WHERE user_id = {user_id}
                AND CV.comment_id = CO.comment_id
        ) AS "option", (
            (
                SELECT COUNT(*) 
                FROM "App_commentvote" CV 
                WHERE option='Up' 
                    AND CV.comment_id = CO.comment_id
            ) - (
                SELECT COUNT(*) 
                FROM "App_commentvote" CV 
                WHERE option='Down' 
                AND CV.comment_id = CO.comment_id
            )
        ) AS "votes"
        FROM "App_comment" CO, "App_user" US
        WHERE CO.user_id = US.user_id
            AND post_id = {post_id}
        ORDER BY votes DESC
    ''')

    comments = [{
        'comment': comment[0],
        'comment_id': comment[1],
        'date_posted': comment[2],
        'user_id': comment[3],
        'username': comment[4],
        'current_vote': comment[5],
        'votes': comment[6]
    } for comment in comments]

    context = {
        'title': 'Post',
        'post': post,
        'current_vote': current_vote,
        'vote_error_msg': request.session.get('vote_error_msg'),
        'comments': comments
    }

    if 'vote_error_msg' in request.session:
        del request.session['vote_error_msg']
        
    return render(request, 'App/post.html', context=context)


