import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username='my_user', password=string_password)

        # Usuario abri a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuario digita o user e a sua senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuario envia o formulario
        form.submit ()

        # Usuario ve a messagem de login com sucesso e seu nome
        self.assertIn(
            f'you are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        #End test
    

    def test_login_crete_raises_404_if_not_POST_method(self):
        # Usuario coloca uma url get
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        # Usuario ve o erro
        self.assertIn(
            'Not Found', 
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # End test

    
    def test_form_login_is_invalid(self):
        # Usuario abri a pagina de login 
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # E tenta enviar valores vazios
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('  ')
        password.send_keys('  ')

        # Enviar o formulario
        form.submit()

        # Ve uma mensagem de erro na tela
        self.assertIn(
            'INVALID USERNAME OR PASSWORD',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # End test


    def test_form_login_invalid_credentials(self):
        # Usuario abri a pagina de login 
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuario ve o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # E tenta enviar valores com dados que nao correspondem
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # Enviar o formulario
        form.submit()

        # Ve uma mensagem de erro na tela
        self.assertIn(
            'INVALID CREDENTIALS',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # End test


