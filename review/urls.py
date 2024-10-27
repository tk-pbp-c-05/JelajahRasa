from django.urls import path
from review.views import food_reviews, create_review, delete_review

urlpatterns = [
    path('food/<uuid:food_id>/', food_reviews, name='food_reviews'),
    path('food/<uuid:food_id>/create-review/', create_review, name='create_review'),
    path('food/<int:review_id>/delete', delete_review, name='delete_review'),
]