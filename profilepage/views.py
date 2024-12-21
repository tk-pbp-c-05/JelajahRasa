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
    
# API untuk flutter
def get_user_profile_api(request, username):
    """API endpoint untuk mendapatkan data profil pengguna"""
    try:
        user = get_object_or_404(CustomUser, username=username)
        response_data = {
            'success': True,
            'user_profile': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'location': user.location,
                'image_url': user.image_url,
                'is_admin': user.is_admin,
            },
            'statistics': {
                'favorite_dishes_count': FavoriteDish.objects.filter(user=user).count(),
                'reviews_count': Review.objects.filter(user=user).count(),
                'comments_count': Comment.objects.filter(user=user).count(),
            }
        }
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def get_user_favorites_api(request, username):
    """API endpoint untuk mendapatkan daftar makanan favorit pengguna"""
    try:
        user = get_object_or_404(CustomUser, username=username)
        favorite_dishes = FavoriteDish.objects.filter(user=user)
        dishes_data = [{
            'name': dish.name,
            'category': dish.category,
            'flavor': dish.flavor,
            'price': float(dish.price),
            'vendor_name': dish.vendor_name,
            'image': dish.image.url if dish.image else None,
        } for dish in favorite_dishes]
        
        return JsonResponse({
            'success': True,
            'favorite_dishes': dishes_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def get_user_reviews_api(request, username):
    """API endpoint untuk mendapatkan daftar review pengguna"""
    try:
        user = get_object_or_404(CustomUser, username=username)
        reviews = Review.objects.filter(user=user)
        reviews_data = [{
            'dish_name': review.dish.name if review.dish else None,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat(),
        } for review in reviews]
        
        return JsonResponse({
            'success': True,
            'reviews': reviews_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def get_user_comments_api(request, username):
    """API endpoint untuk mendapatkan daftar komentar pengguna"""
    try:
        user = get_object_or_404(CustomUser, username=username)
        comments = Comment.objects.filter(user=user)
        comments_data = [{
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
        } for comment in comments]
        
        return JsonResponse({
            'success': True,
            'comments': comments_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)