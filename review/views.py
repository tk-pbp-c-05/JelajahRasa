from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Review
from main.models import Food
from django.contrib import messages

# Create your views here.
def food_reviews(request, food_id):
    food = get_object_or_404(Food, uuid=food_id)
    reviews = food.reviews.all().order_by('-timestamp')[:5]

    context = {
        'food': food,
        'reviews': reviews,
    }
    return render(request, 'review.html', context)

@csrf_exempt
@require_POST
@login_required
def create_review(request, food_id):
    food = get_object_or_404(Food, uuid=food_id)
    comment = request.POST.get("comment")
    rating = request.POST.get("rating")
    
    if not comment or not rating:
        return JsonResponse({'error': 'Both fields cannot be empty.'}, status=400)
    
    user = request.user
    
    new_review = Review(
        food=food,
        user=user,
        comment=comment,
        rating=rating,
        timestamp=timezone.now()
    )
    new_review.save()
    
    food.update_average_rating()
    
    formatted_timestamp = new_review.timestamp.strftime("%B %d, %Y, %I:%M %p")
    
    return JsonResponse({
        'message': 'Review submitted successfully.',
        'user': user.username,
        'comment': comment,
        'rating': rating,
        'timestamp': formatted_timestamp  # Convert timestamp to string
    }, status=201)
    
@user_passes_test(lambda u: u.is_superuser)
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('food_detail', food_uuid=review.food.uuid)  # Adjust the redirect as needed

    return redirect('food_detail', food_uuid=review.food.uuid)