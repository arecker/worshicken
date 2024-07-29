from django.test import TestCase
from django.urls import reverse

from db.models import User, Invitation


class RegisterViewTestCase(TestCase):
    url = reverse('register')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Register an account to access worshicken.' in str(response.content))

        # Current user should be anonymous
        self.assertTrue(response.context['user'].is_anonymous)

    def test_good_post(self):
        # make an invitation
        Invitation.objects.create(email='test@testerson.com')

        response = self.client.post(self.url, data={
            'email': 'test@testerson.com',
            'password': 'test',
            'password_confirm': 'test',
        }, follow=True)

        # User should be created
        user = User.objects.get(email='test@testerson.com')
        self.assertEqual(response.context['user'], user)

        # Invitation should be inactive
        invitations = Invitation.objects.filter(email='test@testerson.com')
        self.assertEqual(invitations.count(), 1)
        self.assertFalse(invitations[0].is_active)

        # User should be logged in
        self.assertTrue(response.context['user'].is_authenticated)

        # Should have redirected home
        self.assertEqual(response.context['request'].path, '/')
