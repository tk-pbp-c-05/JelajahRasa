import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from .models import Review
from main.models import Food

# Create your views here.
def food_reviews(request, food_id):
    food = get_object_or_404(Food, uuid=food_id)
    
    order = request.GET.get('order', 'newest')  
    if order == 'oldest':
        reviews = food.reviews.all().order_by('timestamp')
    else:
        reviews = food.reviews.all().order_by('-timestamp')

    context = {
        'food': food,
        'reviews': reviews,
        'current_order': order,
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
    existing_review = Review.objects.filter(food=food, user=user).first()
    if existing_review:
        return JsonResponse({'error': 'You have already reviewed this food.'}, status=400)

    new_review = Review(
        food=food,
        user=user,
        comment=comment,
        rating=rating,
        timestamp=timezone.now()
    )
    new_review.save()
    
    food.update_average_rating()
    new_average_rating = food.average_rating
    
    formatted_timestamp = new_review.timestamp.strftime("%B %d, %Y, %I:%M %p")
    
    return JsonResponse({
        'user': user.username,
        'comment': comment,
        'rating': rating,
        'timestamp': formatted_timestamp,  # Convert timestamp to string
        'uuid': new_review.uuid,
        'average_rating': new_average_rating
    }, status=201)
    
@login_required
@require_POST
def update_review(request, review_id):
    review = get_object_or_404(Review, uuid=review_id)
    
    # Ensure that the user is the one who created the review
    if review.user != request.user:
        return JsonResponse({'error': 'You are not allowed to update this review.'}, status=403)
    
    comment = request.POST.get("comment")
    rating = request.POST.get("rating")
    
    if not comment or not rating:
        return JsonResponse({'error': 'Both fields cannot be empty.'}, status=400)
    
    # Update review fields
    review.comment = comment
    review.rating = rating
    review.timestamp = timezone.now()  # Optionally update the timestamp
    review.save()
    
    review.food.update_average_rating()
    new_average_rating = review.food.average_rating
    
    formatted_timestamp = review.timestamp.strftime("%B %d, %Y, %I:%M %p")
    
    return JsonResponse({
        'user': review.user.username,
        'comment': review.comment,
        'rating': review.rating,
        'timestamp': formatted_timestamp,
        'uuid': review.uuid,
        'average_rating': new_average_rating
    }, status=200)

def delete_review(request, review_id):
    review = get_object_or_404(Review, uuid=review_id)
    food = review.food
    
    if not request.user.is_admin and review.user != request.user:
        return HttpResponseForbidden("You do not have permission to delete this review.")
    
    if request.method == 'POST':
        review.delete()
        food.update_average_rating()
        return redirect('review:food_reviews', food_id=review.food.uuid)  # Adjust the redirect as needed

    return redirect('review:food_reviews', food_id=review.food.uuid)

def show_json(request, food_id):
    data = Review.objects.filter(food=food_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_review = Review.objects.create(
            user=request.user,
            comment=data["comment"],
            rating=int(data["rating"])
        )

        new_review.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_review_flutter(request, uuid):
    if request.method == "POST":  # Gunakan POST untuk menggantikan DELETE
        review = get_object_or_404(Review, pk=uuid, user=request.user)
        review.delete()
        return JsonResponse({"status": True, "message": "Review deleted successfully."})
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def update_review_flutter(request, uuid):
    if request.method == 'POST':
        data = json.loads(request.body)
        review = get_object_or_404(Review, pk=uuid, user=request.user)

        review.comment = data.get('comment', review.comment)
        review.rating = int(data.get('rating', review.rating))

        review.save()
        return JsonResponse({"status": "success", "message": "Review updated successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)