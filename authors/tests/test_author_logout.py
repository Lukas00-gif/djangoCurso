from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn('Invalid logout request!!!', response.content.decode('utf-8'))


    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'), 
            follow=True,
            data={
                'username': 'another_user'
            }
        )

        self.assertIn('Invalid logout user!!!', response.content.decode('utf-8'))


    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'), 
            follow=True,
            data={
                'username': 'my_user'
            }
        )

        self.assertIn('Logged out successfully', response.content.decode('utf-8'))



