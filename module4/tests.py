from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from module4.models import NewDish
from main.models import Food

User = get_user_model()

class AddDishViewTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', email='admin@test.com', password='admin123', is_admin=True)
        self.regular_user = User.objects.create_user(username='user', email='user@test.com', password='user123')

    def test_add_dish_as_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('module4:add_dish'), {
            'name': 'Test Dish',
            'flavor': 'sweet',
            'category': 'food',
            'price': 10000,
            'vendor_name': 'Vendor A',
            'map_link': 'https://maps.example.com',
            'address': 'Street 123',
            'image': 'image.jpg'
        })

        self.assertEqual(response.status_code, 302)
        new_dish = NewDish.objects.get(name='Test Dish')
        self.assertTrue(new_dish.is_approved)
        self.assertTrue(Food.objects.filter(uuid=new_dish.uuid).exists())

    def test_add_dish_as_regular_user(self):
        self.client.login(username='user', password='user123')
        response = self.client.post(reverse('module4:add_dish'), {
            'name': 'User Dish',
            'flavor': 'salty',
            'category': 'beverage',
            'price': 20000,
            'vendor_name': 'Vendor B',
            'map_link': 'https://maps.example.com',
            'address': 'Street 456',
            'image': 'image.jpg'
        })

        self.assertEqual(response.status_code, 302)
        user_dish = NewDish.objects.get(name='User Dish')
        self.assertFalse(user_dish.is_approved)
        self.assertFalse(Food.objects.filter(uuid=user_dish.uuid).exists())


class CheckDishViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', email='admin@test.com', password='admin123', is_admin=True)
        self.regular_user = User.objects.create_user(username='user', email='user@test.com', password='user123')
        
        self.pending_dish = NewDish.objects.create(
            name='Pending Dish',
            flavor='sweet',
            category='food',
            price=15000,
            vendor_name='Vendor C',
            map_link='https://maps.example.com',
            address='Street 789',
            image='image.jpg',
            is_approved=False
        )

    def test_check_dish_as_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('module4:check_dish'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pending Dish')

    def test_check_dish_as_regular_user(self):
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('module4:check_dish'))
        self.assertEqual(response.status_code, 302)


class ApproveDishViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', email='admin@test.com', password='admin123', is_admin=True)
        self.regular_user = User.objects.create_user(username='user', email='user@test.com', password='user123')

        self.pending_dish = NewDish.objects.create(
            name='Pending Dish',
            flavor='salty',
            category='beverage',
            price=15000,
            vendor_name='Vendor C',
            map_link='https://maps.example.com',
            address='Street 789',
            image='image.jpg',
            is_approved=False
        )

    def test_approve_dish_as_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('module4:approve_dish', args=[self.pending_dish.uuid]), {
            'action': 'approve'
        })
        self.assertEqual(response.status_code, 200)
        self.pending_dish.refresh_from_db()
        self.assertTrue(self.pending_dish.is_approved)
        self.assertTrue(Food.objects.filter(uuid=self.pending_dish.uuid).exists())

    def test_delete_dish_as_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('module4:approve_dish', args=[self.pending_dish.uuid]), {
            'action': 'delete'
        })

        self.assertEqual(response.status_code, 200)
        with self.assertRaises(NewDish.DoesNotExist):
            NewDish.objects.get(uuid=self.pending_dish.uuid)

    def test_approve_dish_as_regular_user(self):
        self.client.login(username='user', password='user123')
        response = self.client.post(reverse('module4:approve_dish', args=[self.pending_dish.uuid]), {
            'action': 'approve'
        })

        self.assertEqual(response.status_code, 403)