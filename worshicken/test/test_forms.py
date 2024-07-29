from django.test import TestCase

from .. import forms


class RegisterFormTest(TestCase):
    def test_it(self):
        form = forms.Register(data={
            'email': 'alex@test.com',
            'password_1': 'test1',
            'password_2': 'test2',
        })

        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.non_field_errors()), 1)
        self.assertEqual(form.non_field_errors(), ['Passwords do not match!'])
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['__all__'], ['Passwords do not match!'])
