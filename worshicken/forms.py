from django import forms
from django.forms import ValidationError
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.utils.safestring import mark_safe

from db import models


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Password (confirm)')

    def __init__(self, *args, **kwargs):
        # accept an "instance" kwarg and do nothing with it
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    def validate_passwords_match(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Passwords do not match!')

    def validate_invited(self):
        email = self.cleaned_data['email']
        self.invitations = models.Invitation.objects.filter(email=email, is_active=True)
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

    def save(self, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # Create the user
        user = models.User.objects.create_user(email)
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
    is_sound = forms.BooleanField(label='Sound help?', required=False)
    is_slides = forms.BooleanField(label='Powerpoint help?', required=False)
    instruments = forms.ModelMultipleChoiceField(
        queryset=models.Instrument.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, data, instance: models.User, **kwargs):
        self.instance = instance

        super().__init__(data=data, initial={
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'korean_name': instance.korean_name,
            'is_singer': instance.is_singer,
            'is_sound': instance.is_sound,
            'is_slides': instance.is_slides,
            'instruments': instance.instruments.all(),
        })

    def save(self, **kwargs):
        self.instance.first_name = self.cleaned_data['first_name']
        self.instance.last_name = self.cleaned_data['last_name']
        self.instance.korean_name = self.cleaned_data['korean_name']
        self.instance.is_singer = self.cleaned_data['is_singer']
        self.instance.is_sound = self.cleaned_data['is_sound']
        self.instance.is_slides = self.cleaned_data['is_slides']
        self.instance.instruments.set(self.cleaned_data['instruments'])
        self.instance.save()
        return self.instance


class BreakForm(forms.ModelForm):
    class Meta:
        model = models.Break
        fields = ['start', 'end', 'reason']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        today = timezone.now().date()

        if start and end:
            if end < start:
                raise ValidationError('The end date cannot be before the start date.')

            if end < today:
                raise ValidationError('The end date must be in the future.')

        return cleaned_data


class InvitationForm(forms.ModelForm):
    class Meta:
        model = models.Invitation
        fields = ['email']


class InstrumentForm(forms.ModelForm):
    musicians = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = models.Instrument
        fields = ['name', 'musicians']


class SongForm(forms.ModelForm):
    class Meta:
        model = models.Song
        fields = ['title']


SongChartFormSet = inlineformset_factory(
    models.Song,
    models.SongChart,
    fields=['key', 'pitch', 'file'],
    extra=1,
    can_delete=True
)


class SetTemplateForm(forms.ModelForm):
    class Meta:
        model = models.SetTemplate
        fields = ['name', 'instruments']
        widgets = {
            'instruments': forms.CheckboxSelectMultiple(),
        }


class SongWithChartsForm:
    '''A wrapper that makes a Form + FormSet look like a single Form.'''
    def __init__(self, data=None, files=None, instance=None):
        self.instance = instance
        self.form = SongForm(data, instance=instance)
        self.formset = SongChartFormSet(data, files, instance=instance)

    def is_valid(self) -> bool:
        return self.form.is_valid() and self.formset.is_valid()

    def as_p(self):
        html = self.form.as_p()
        html += "<h3>Charts</h3>"
        html += self.formset.management_form.as_p()
        for form in self.formset:
            html += f"<div class='chart-row'>{form.as_p()}</div><hr>"
        return mark_safe(html)

    def save(self, commit=True):
        song = self.form.save(commit=commit)
        self.formset.instance = song
        self.formset.save()
        return song

    @property
    def errors(self):
        return self.form.errors or self.formset.errors
