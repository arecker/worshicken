from django import forms
from django.forms.models import inlineformset_factory, modelform_factory

from db.models import Instrument, User, Song, SongChart, Invitation


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Password (confirm)')

    def validate_passwords_match(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Passwords do not match!')

    def validate_invited(self):
        email = self.cleaned_data['email']
        self.invitations = Invitation.objects.filter(email=email, is_active=True)
        if self.invitations.count() < 1:
            raise forms.ValidationError('You have not received an invitation to register, please contact admin.')

    def is_valid(self):
        if not super().is_valid():
            return False
        try:
            self.validate_passwords_match()
            self.validate_invited()
        except forms.ValidationError as e:
            self.add_error(None, e)
            return False
        return True

    def save(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # Create the user
        user = User.objects.create_user(email)
        user.set_password(password)
        user.save()

        # Clear the invitations
        self.invitations.update(is_active=False)

        return user


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=80, required=False)
    last_name = forms.CharField(max_length=80, required=False)
    korean_name = forms.CharField(max_length=80, required=False)
    is_singer = forms.BooleanField(label='Singer?', required=False)
    instruments = forms.ModelMultipleChoiceField(
        queryset=Instrument.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, data, instance: User):
        self.instance = instance

        super().__init__(data=data, initial={
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'korean_name': instance.korean_name,
            'is_singer': instance.is_singer,
            'instruments': instance.instruments.all(),
        })

    def save(self):
        self.instance.first_name = self.cleaned_data['first_name']
        self.instance.last_name = self.cleaned_data['last_name']
        self.instance.korean_name = self.cleaned_data['korean_name']
        self.instance.is_singer = self.cleaned_data['is_singer']
        self.instance.instruments.set(self.cleaned_data['instruments'])
        self.instance.save()


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']


class InstrumentForm(forms.ModelForm):
    musicians = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Instrument
        fields = ['name', 'musicians']


SongForm = modelform_factory(
    Song,
    fields=['title']
)


SongChartFormset = inlineformset_factory(
    Song,
    SongChart,
    extra=1,
    can_delete=True,
    exclude=[],
)
