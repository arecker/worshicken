from django.test import TestCase
from django.forms import ValidationError

from .. import forms
from db.models import Invitation


class RegisterFormTestCase(TestCase):
    def setUp(self):
        self.invitation = Invitation.objects.create(email='test@test.com')

    def tearDown(self):
        self.invitation.delete()

    def test_is_valid(self):
        form = forms.RegisterForm(data={
            'email': 'test@test.com',
            'password': 'test',
            'password_confirm': 'test',
        })
        self.assertTrue(form.is_valid())

        form = forms.RegisterForm(data={
            'email': None,
            'password': 'test',
            'password_confirm': 'test',
        })
        self.assertFalse(form.is_valid())

        form = forms.RegisterForm(data={
            'email': 'test@test.com',
            'password': 'test',
            'password_confirm': 'testly',
        })
        self.assertFalse(form.is_valid())

    def test_validate_passwords_match(self):
        form = forms.RegisterForm(data={
            'email': 'test@test.com',
            'password': 'test1',
            'password_confirm': 'test2',
        })
        form.full_clean()

        with self.assertRaisesRegex(ValidationError, 'Passwords do not match!'):
            form.validate_passwords_match()
