from django.urls import path
from review.views import food_reviews, create_review, update_review, delete_review, show_json, create_review_flutter, update_review_flutter, delete_review_flutter

app_name = 'review'

urlpatterns = [
    path('food/<uuid:food_id>/', food_reviews, name='food_reviews'),
    path('food/<uuid:food_id>/create-review/', create_review, name='create_review'),
    path('food/<uuid:review_id>/update-review', update_review, name='update_review'),
    path('food/<uuid:review_id>/delete-review', delete_review, name='delete_review'),
    path('food/<uuid:food_id>/create-review-flutter/', create_review, name='create_review_flutter'),
    path('food/<uuid:review_id>/update-review-flutter', update_review, name='update_review_flutter'),
    path('food/<uuid:review_id>/delete-review-flutter', delete_review, name='delete_review_flutter'),
    path('food/<uuid:review_id>/json/', show_json, name='show_json'),
]