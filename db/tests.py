from django.test import TestCase

from .models import User


class UserTestCase(TestCase):
    def test_create_user(self):
        """Create a regular user the ORM."""

        User.objects.create_user('larry@stooges.biz', password='password')
        User.objects.create_user('mo@stooges.biz', password='password')
        User.objects.create_user('curly@stooges.biz', password='password')

        users = User.objects.all()
        self.assertEqual(len(users), 3)
        self.assertTrue(all([not u.is_superuser for u in users]))

    def test_create_superuser(self):
        """Create a super user using the ORM."""

        User.objects.create_superuser('alex@stooges.com', password='password')
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertTrue(user.is_superuser)
