from django.shortcuts import render, redirect
from ..forms import CreatePost
from ..models import Post

def create(request):

    user_id = request.session.get('user_id', -1)
    if user_id == -1:
        return redirect('home')

    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            
            new_post = Post(
                status='Open',
                user_id=user_id,
                **form.cleaned_data
            )
            new_post.save()

        else:
            print(form.errors)

    context = {}
    return render(request, 'App/create.html', context=context)