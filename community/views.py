from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Comment, Reply
from main.models import Food, CustomUser
from .forms import CommentForm, ReplyForm

def community_home(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'community/home.html', {'comments': comments})

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            if form.cleaned_data['food_name']:
                food = get_object_or_404(Food, name=form.cleaned_data['food_name'])
                comment.food = food
            comment.save()
            return redirect('community_home')
    else:
        form = CommentForm()
    return render(request, 'community/add_comment.html', {'form': form})

@login_required
def edit_comment(request, uuid):
    comment = get_object_or_404(Comment, uuid=uuid, user=request.user)
    if not comment.is_editable:
        return redirect('community_home')
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('community_home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'community/edit_comment.html', {'form': form})

@login_required
def add_reply(request, comment_uuid):
    comment = get_object_or_404(Comment, uuid=comment_uuid)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            return redirect('community_home')
    else:
        form = ReplyForm()
    return render(request, 'community/add_reply.html', {'form': form, 'comment': comment})

def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    comments = user.comments.all().order_by('-created_at')
    return render(request, 'community/user_profile.html', {'profile_user': user, 'comments': comments})