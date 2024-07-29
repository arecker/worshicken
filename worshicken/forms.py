from django import forms


class Register(forms.Form):
    email = forms.EmailField(required=True)
    password_1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        data = super().clean()
        if data['password_1'] != data['password_2']:
            raise forms.ValidationError('Passwords do not match!')
        return data
