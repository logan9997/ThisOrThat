from django.shortcuts import render, redirect
from ..forms import CreatePost
from ..models import Post
from ..utils import FormRestrictions
from django.conf import settings
import os

def create(request, post_id=None):

    user_id = request.session.get('user_id', -1)
    if user_id == -1:
        return redirect('home')

    # if user is editting a post, get the values from the post to set as values
    # in the html form
    edit_post_values = {}
    if post_id != None:
        edit_post_values = list(Post.objects.filter(post_id=post_id).values())[0]
        for image in ['image_one', 'image_two']:
            if edit_post_values[image] != None:
                edit_post_values[image] = os.path.join(settings.MEDIA_URL, edit_post_values[image])

    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():

            print(repr(form.cleaned_data.get('main_description')))
            str

            new = {}
            for k, v in form.cleaned_data.items():
                if 'remove_image' in k and v == 'REMOVE':
                    new[f'image_{k.replace("remove_image_", "")}'] = None
                    continue
                if v not in ['', None]:
                    new[k] = v
        
            form.cleaned_data = new
            
            if post_id != None:
                update_post = Post.objects.get(post_id=post_id)
                for k, v in form.cleaned_data.items():
                    setattr(update_post, k, v)
                update_post.save()
            else:
                new_post = Post(
                    status='Open',
                    user_id=user_id,
                    **form.cleaned_data
                )
                new_post.save()
                post_id = new_post.post_id

            return redirect('post', post_id)
        else:
            print(form.errors)

    context = {
        'input_restrictions': FormRestrictions.create_post(),
        'edit_post_values':edit_post_values,
        'post_id': post_id
    }
    return render(request, 'App/create.html', context=context)


