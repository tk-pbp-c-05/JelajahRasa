from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm
from main.models import CustomUser
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile
from MyFavoriteDishes.models import FavoriteDish

# Create your views here.

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    favorite_dishes = FavoriteDish.objects.filter(user=profile_user)[:6]  # Get up to 6 favorite dishes
    context = {
        'profile_user': profile_user,
        'user': request.user,
        'favorite_dishes': favorite_dishes,
        'favorite_dishes_count': profile_user.profile.get_favorite_dishes_count(),
    }
    return render(request, 'profile.html', context)

@login_required
@require_POST
def edit_profile(request, username):
    if request.user.username != username:
        return JsonResponse({'success': False, 'message': 'You can only edit your own profile'}, status=403)

    user = request.user
    user.first_name = request.POST.get('first_name', '')
    user.last_name = request.POST.get('last_name', '')
    
    # Assuming these fields exist in your CustomUser model
    user.location = request.POST.get('location', '')
    user.image_url = request.POST.get('image_url', '')
    
    try:
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.description = request.POST.get('description', '')
        profile.save()

        return JsonResponse({
            'success': True,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'location': user.location,
            'image_url': user.image_url,
            'description': profile.description,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
