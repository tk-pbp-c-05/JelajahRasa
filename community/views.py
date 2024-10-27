from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Comment, Reply
from main.models import Food, CustomUser
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Comment, Reply
from .forms import CommentForm, ReplyForm
from main.models import Food, CustomUser
from django.http import JsonResponse


@login_required
def community_home(request):
    comments = Comment.objects.all().order_by('-created_at')
    foods = Food.objects.all()
    context = {
        'comments': comments,
        'foods': foods,
        'user': request.user
    }
    return render(request, 'community.html', context)

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            comments = Comment.objects.all().order_by('-created_at')
            html = render_to_string('comments_list.html', {'comments': comments, 'user': request.user})
            return JsonResponse({'success': True, 'html': html})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def add_reply(request, comment_uuid):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, uuid=comment_uuid)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            comments = Comment.objects.all().order_by('-created_at')
            html = render_to_string('comments_list.html', {'comments': comments, 'user': request.user})
            return JsonResponse({'success': True, 'html': html})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def edit_comment(request, uuid):
    comment = get_object_or_404(Comment, uuid=uuid)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            comments = Comment.objects.all().order_by('-created_at')
            html = render_to_string('comments_list.html', {'comments': comments, 'user': request.user})
            return JsonResponse({'success': True, 'html': html})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_comment(request, uuid):
    comment = get_object_or_404(Comment, uuid=uuid)
    if request.user == comment.user:
        comment.delete()
        comments = Comment.objects.all().order_by('-created_at')
        html = render_to_string('comments_list.html', {'comments': comments, 'user': request.user})
        return JsonResponse({'success': True, 'html': html})
    return JsonResponse({'success': False, 'error': 'You are not authorized to delete this comment.'})

@login_required
def delete_reply(request, uuid):
    reply = get_object_or_404(Reply, uuid=uuid)
    if request.user == reply.user:
        reply.delete()
        comments = Comment.objects.all().order_by('-created_at')
        html = render_to_string('comments_list.html', {'comments': comments, 'user': request.user})
        return JsonResponse({'success': True, 'html': html})
    return JsonResponse({'success': False, 'error': 'You are not authorized to delete this reply.'})

@login_required
def comment_detail(request, uuid):
    comment = get_object_or_404(Comment, uuid=uuid)
    context = {
        'comment': comment,
        'replies': comment.replies.all().order_by('created_at')
    }
    return render(request, 'comment_detail.html', context)