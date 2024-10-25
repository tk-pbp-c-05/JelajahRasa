from django.urls import path
from review.views import food_reviews, create_review

urlpatterns = [
    path('food/<int:food_id>/', food_reviews, name='food_review'),
    path('food/<int:food_id>/create-review/', create_review, name='create_review'),
]