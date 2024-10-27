from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from main.models import Food
from review.models import Review
import uuid

class ReviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin', password='password'
        )
        
        self.food = Food.objects.create(uuid=uuid.uuid4(), name="Pizza", average_rating=0)
        self.food_id = self.food.uuid

        self.review = Review.objects.create(
            uuid=uuid.uuid4(),
            food=self.food,
            user=self.user,
            rating=5,
            comment="Great taste!",
            timestamp=now()
        )
        self.review_id = self.review.uuid

    def test_food_reviews_view(self):
        """Test if the food_reviews view returns the correct response."""
        response = self.client.get(reverse('food_reviews', args=[self.food_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')
        self.assertContains(response, "Pizza")

    def test_create_review_success(self):
        """Test if a review is created successfully."""
        self.client.login(username='testuser', password='password')

        data = {'comment': 'Delicious!', 'rating': 4}
        response = self.client.post(
            reverse('create_review', args=[self.food_id]), data=data
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 2)  # One review created in setUp + this one
        self.assertContains(response, 'average_rating')

    def test_create_review_failure(self):
        """Test if empty comment or rating returns an error."""
        self.client.login(username='testuser', password='password')

        data = {'comment': '', 'rating': ''}
        response = self.client.post(
            reverse('create_review', args=[self.food_id]), data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Both fields cannot be empty.'})

    def test_delete_review_by_admin(self):
        """Test if an admin can delete a review."""
        self.client.login(username='admin', password='password')

        response = self.client.post(reverse('delete_review', args=[self.review_id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertEqual(Review.objects.count(), 0)  # Review should be deleted

    def test_delete_review_by_non_admin(self):
        """Test if a non-admin user is denied access to delete a review."""
        self.client.login(username='testuser', password='password')

        response = self.client.post(reverse('delete_review', args=[self.review_id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_review_ordering_newest_first(self):
        """Test if reviews are ordered from newest to oldest."""
        response = self.client.get(reverse('food_reviews', args=[self.food_id]))
        reviews = response.context['reviews']
        self.assertGreater(reviews[0].timestamp, reviews[1].timestamp)

    def test_review_ordering_oldest_first(self):
        """Test if reviews are ordered from oldest to newest."""
        response = self.client.get(reverse('food_reviews', args=[self.food_id]) + '?order=oldest')
        reviews = response.context['reviews']
        self.assertLessEqual(reviews[0].timestamp, reviews[1].timestamp)
