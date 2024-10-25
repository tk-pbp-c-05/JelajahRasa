from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Review
from main.models import Food

# Create your views here.
def food_reviews(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    reviews = food.reviews.all().order_by('-timestamp')[:5]

    context = {
        'food': food,
        'reviews': reviews,
    }
    return render(request, 'review.html', context)

@csrf_exempt
@require_POST
def create_review(request, food_id):
    food = get_object_or_404(Food, id=food_id)
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
    
    return JsonResponse({'message': 'Review submitted successfully.'}, status=201)