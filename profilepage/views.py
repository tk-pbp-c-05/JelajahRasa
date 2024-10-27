from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm
from main.models import CustomUser
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from MyFavoriteDishes.models import FavoriteDish

# Create your views here.

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    favorite_dishes = FavoriteDish.objects.filter(user=profile_user)
    context = {
        'profile_user': profile_user,
        'user': request.user,
        'favorite_dishes': favorite_dishes,
        'favorite_dishes_count': favorite_dishes.count(),
    }
    return render(request, 'profile.html', context)

def all_favorite_dishes(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    dishes = FavoriteDish.objects.filter(user=profile_user)
    
    dishes_data = [
        {
            'name': dish.name,
            'category': dish.category,
            'flavor': dish.flavor,
            'price': f"{dish.price:,.0f}",
            'vendor_name': dish.vendor_name,
            'map_link': dish.map_link,
            'image': dish.image.url if dish.image else None,
        }
        for dish in dishes
    ]
    
    return JsonResponse({'dishes': dishes_data})

@login_required
@require_POST
def edit_profile(request, username):
    if request.user.username != username:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    user = request.user
    user.username = request.POST.get('username', user.username)
    user.first_name = request.POST.get('first_name', user.first_name)
    user.last_name = request.POST.get('last_name', user.last_name)
    user.location = request.POST.get('location', user.location)
    user.image_url = request.POST.get('image_url', user.image_url)
    user.save()

    return JsonResponse({
        'success': True,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'location': user.location,
        'image_url': user.image_url
    })
