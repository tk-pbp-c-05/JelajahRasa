from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm
from main.models import CustomUser
from django.urls import reverse

# Create your views here.

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    context = {
        'profile_user': profile_user,
        'user': request.user,
        # 'favorite_dishes': user.favorite_dishes.all()[:6],  # Assuming a related_name 'favorite_dishes'
        # 'favorite_dishes_count': user.favorite_dishes.count(),
        # 'reviewed_dishes': user.reviews.all()[:6],  # Assuming a related_name 'reviews'
        # 'reviewed_dishes_count': user.reviews.count(),
        # 'forum_comments': user.forum_comments.all()[:6],  # Assuming a related_name 'forum_comments'
        # 'forum_comments_count': user.forum_comments.count(),
    }
    return render(request, 'profile.html', context)

def edit_profile(request, username):
    if request.user != username:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect(reverse('main:show_main'))  # Redirect to homepage
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})
