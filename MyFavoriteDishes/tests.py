import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Food, FavoriteDish

class MyFavoriteDishesTests(TestCase):
    def setUp(self):
        CustomUser = get_user_model()
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password123', email="example@example.com")
        self.food = Food.objects.create(
            name="Test Food",
            flavor="salty",
            category="food",
            vendor_name="Test Vendor",
            price=10000,
            map_link="https://example.com/map",
            address="123 Test St",
            image="https://example.com/image.jpg"
        )
        self.favorite_dish = FavoriteDish.objects.create(
            user=self.user,
            food=self.food,
            name=self.food.name,
            flavor=self.food.flavor,
            category=self.food.category,
            vendor_name=self.food.vendor_name,
            price=self.food.price,
            map_link=self.food.map_link,
            address=self.food.address,
            image=self.food.image
        )

    def test_access_favorite_not_logged_in(self):
        response = self.client.get(reverse('MyFavoriteDishes:access_favorite'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:login'))
    
    def test_add_favorite_post(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('MyFavoriteDishes:add_favorite'), {
            'food': self.food.uuid
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('MyFavoriteDishes:show_favorite'))
        self.assertEqual(FavoriteDish.objects.filter(user=self.user).count(), 2)

    def test_add_fav_dish_ajax(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('MyFavoriteDishes:add_fav_dish_ajax'), {
            'name': 'New Favorite Dish',
            'flavor': 'sweet',
            'category': 'food',
            'vendor_name': 'Vendor Test',
            'price': 5000,
            'map_link': 'https://example.com/newmap',
            'address': '456 Test St',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FavoriteDish.objects.filter(user=self.user).count(), 2)

    def test_delete_favorite_dish(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('MyFavoriteDishes:delete_favorite_dish', args=[self.favorite_dish.uuid]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('MyFavoriteDishes:show_favorite'))
        self.assertEqual(FavoriteDish.objects.filter(user=self.user).count(), 0)
    
    def test_show_json(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.get(reverse('MyFavoriteDishes:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['name'], 'Test Food')



