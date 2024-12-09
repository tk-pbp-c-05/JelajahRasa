from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm
from main.models import CustomUser
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from MyFavoriteDishes.models import FavoriteDish
from review.models import Review
from community.models import Comment
from profilepage.models import UserProfile
# Create your views here.

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    favorite_dishes = FavoriteDish.objects.filter(user=profile_user)
    reviews = Review.objects.filter(user=profile_user)
    comments = Comment.objects.filter(user=profile_user)
    context = {
        'profile_user': profile_user,
        'user': request.user,
        'favorite_dishes': favorite_dishes,
        'favorite_dishes_count': favorite_dishes.count(),
        'reviews': reviews,
        'reviews_count': reviews.count(),
        'comments': comments,
        'comments_count': comments.count(),
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
    user.first_name = request.POST.get('first_name', user.first_name)
    user.last_name = request.POST.get('last_name', user.last_name)
    user.location = request.POST.get('location', user.location)
    user.image_url = request.POST.get('image_url', user.image_url)
    user.save()

    return JsonResponse({
        'success': True,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'location': user.location,
        'image_url': user.image_url,
    })
    
def get_user_data_api(request, username):
    """API endpoint untuk mendapatkan data profil dan aktivitas pengguna"""
    try:
        user = get_object_or_404(CustomUser, username=username)
        
        # Mengambil data favorite dishes
        favorite_dishes = FavoriteDish.objects.filter(user=user)
        dishes_data = [{
            'name': dish.name,
            'category': dish.category,
            'flavor': dish.flavor,
            'price': float(dish.price),
            'vendor_name': dish.vendor_name,
            'image': dish.image.url if dish.image else None,
        } for dish in favorite_dishes]
        
        # Mengambil data reviews
        reviews = Review.objects.filter(user=user)
        reviews_data = [{
            'dish_name': review.dish.name if review.dish else None,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat(),
        } for review in reviews]
        
        # Mengambil data comments
        comments = Comment.objects.filter(user=user)
        comments_data = [{
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
        } for comment in comments]
        
        response_data = {
            'success': True,
            'user_profile': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'location': user.location,
                'image_url': user.image_url,
            },
            'statistics': {
                'favorite_dishes_count': favorite_dishes.count(),
                'reviews_count': reviews.count(),
                'comments_count': comments.count(),
            },
            'favorite_dishes': dishes_data,
            'reviews': reviews_data,
            'comments': comments_data,
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
