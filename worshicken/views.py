from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView, FormView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail

from db.models import Member, Invitation
from . import forms


class Home(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "home.html"


class Register(FormView):
    template_name = "register.html"
    form_class = forms.Register
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email, password = form.cleaned_data['email'], form.cleaned_data['password_1']

        # Find a matching invitation
        try:
            invitation = Invitation.objects.get(email=email, is_accepted=False)
        except Invitation.DoesNotExist:
            return HttpResponseBadRequest('You do not have an invitation to register.')

        # Create the user
        member = Member.objects.create_user(email=invitation.email, password=password)

        # Accept the invite
        invitation.is_accepted = True
        invitation.accepted = timezone.now()
        invitation.save()

        # Log the user in
        member = authenticate(self.request, email=email, password=password)
        if not member:
            raise RuntimeError(f'could not authenticate {email}')
        login(self.request, member)

        return super().form_valid(form)


class Profile(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = 'profile.html'
    success_url = reverse_lazy('home')
    fields = (
        'first_name',
        'last_name',
        'korean_name',
        'is_singer',
    )

    def get_object(self):
        return self.request.user


class Invitations(LoginRequiredMixin, ListView):
    model = Invitation
    template_name = 'invitations.html'


class InvitationCreate(LoginRequiredMixin, CreateView):
    model = Invitation
    fields = ('email', )
    template_name = 'invitation-create.html'
    success_url = reverse_lazy('invitations')

    def form_valid(self, form):
        send_mail(
            subject='You Have Been Invited to Join Worshicken',
            from_email='admin@localhost',
            recipient_list=[form.cleaned_data['email']],
            message='''
You have been invited to join Worshicken!  You can register a profile here:
http://localhost:8000/register/
            '''.strip()
        )
        return super().form_valid(form)


class InvitationDelete(LoginRequiredMixin, DeleteView):
    model = Invitation
    template_name = 'invitation-delete.html'
    success_url = reverse_lazy('invitations')
