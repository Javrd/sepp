from django.test import TestCase, RequestFactory
from mvp.models import User

class test_login(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.duplicate = {
            'username': 'duplicate',
            'password': 'secrett'}
        self.credentialsBadUsername = {
            'username': 'testuserbadbadbad',
            'password': 'secret'}
        self.credentialsBadPass = {
            'username': 'testuser',
            'password': 'secretbadbadbad'}
        User.objects.create_user(**self.credentials)

    def test_LoginPositive(self):
        # Manda las credenciales al login
        response = self.client.post('/login', self.credentials, follow=True)
        # Ya deberia estar logueado
        self.assertTrue(response.context['user'].is_active)

    def test_LoginBadPass(self):
        response2 = self.client.post('/login', self.credentialsBadUsername, follow=True)
        self.assertFalse(response2.context['user'].is_active)

    def test_LoginBadUsername(self):
        response3 = self.client.post('/login', self.credentialsBadPass, follow=True)
        self.assertFalse(response3.context['user'].is_active)
