from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from .models import Meal
from .forms import UserLoginForms
# Create your tests here.

class MealModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Meal.objects.create(
            name="test meal",
            description="this is a test meal",
            price=20,
            available=True,
            stock=3,
        )

    def test_meal_name(self):
        meal = Meal.objects.get(id=1)
        self.assertEqual(meal.name, "test meal")

    def test_stock_count(self):
        meal = Meal.objects.get(id=1)
        self.assertEqual(meal.stock, 3)


class ViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    def test_details_view(self):
        user = User.objects.create(username="name")
        user.set_password('password')

        user.save()

        response = self.client.login(username="name", password="password")

        self.assertTrue(response)

    def tast_details_view_fails(self):
        user = User.objects.create(username="name")
        user.set_password('password')

        user.save()

        response = self.client.login(username="name", password="password2")

        self.assertFalse(response)


class FormsTest(TestCase):
    def test_login_form_user_name_is_required(self):
        form = UserLoginForms()

        self.assertTrue(form.fields['username'].required)

    def test_valid_login_form(self):
        User.objects.create_user(username="name", password="password")

        form = UserLoginForms(data={
            "username": "name",
            "password": "password",
        })

        self.assertTrue(form.is_valid())


class ClientTest(TestCase):
    def test_login(self):
        user = User.objects.create(username="name")
        user.set_password('password')

        user.save()

        c = Client()

        c.post("/login/", {
            "username": "name",
            "password": "password",
        })

        self.assertTrue(get_user(c).is_authenticated)
