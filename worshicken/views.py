import dataclasses
import typing

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.utils import timezone
from django import urls
from django.http import Http404

from db import models
from . import forms


@dataclasses.dataclass
class ThingDetailHandler:
    model_class: typing.Type
    form_class: typing.Type
    success_url: str
    extra_context: dict = dataclasses.field(default_factory=dict)
    pre_save: typing.Optional[typing.Callable] = None
    post_save: typing.Optional[typing.Callable] = None
    template_name: str = 'thing-detail.html'


def thing_detail(handler: ThingDetailHandler, request, pk=None):
    if pk:
        try:
            instance = handler.model_class.objects.get(pk=pk)
        except handler.model_class.DoesNotExist:
            raise Http404()
    else:
        instance = None

    if request.method == 'POST':
        form = handler.form_class(request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            if handler.pre_save:
                handler.pre_save(instance=instance, form=form)
            instance.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            if handler.post_save:
                handler.post_save(instance=instance, form=form)
            return redirect(handler.success_url)
    else:
        form = handler.form_class(None, instance=instance)

    context = {'form': form, 'instance': instance}
    context.update(handler.extra_context)
    return render(request, handler.template_name, context=context)


def thing_delete(model_class, success_url, request, pk):
    instance = model_class.objects.get(pk=pk)
    if request.method == 'POST':
        instance.delete()
        return redirect(success_url)
    return render(request, 'thing-delete.html', context={'thing': instance})


@login_required
@require_http_methods(['GET', 'POST'])
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'logout.html')


@login_required
@require_http_methods(['GET'])
def home(request):
    return render(request, 'home.html', {})


@require_http_methods(['GET', 'POST'])
def register(request):
    def post_save(instance=None, form=None):
        user = authenticate(request, username=instance.email, password=form.cleaned_data['password'])
        if not user:
            raise ValueError(f'could not authenticate {form.cleaned_data["email"]}')
        login(request, user)

    handler = ThingDetailHandler(
        model_class=models.User,
        form_class=forms.RegisterForm,
        success_url='home',
        post_save=post_save,
        template_name='register.html',
    )

    return thing_detail(handler, request, pk=None)


@login_required
@require_http_methods(['GET'])
def user_list(request):
    return render(request, 'user-list.html', context={
        'users': models.User.objects.all(),
        'invitations': models.Invitation.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def user_detail(request, pk):
    if not request.user.is_superuser and request.user.pk != pk:
        return HttpResponseForbidden()

    handler = ThingDetailHandler(
        model_class=models.User,
        form_class=forms.UserForm,
        success_url='user-list',
        template_name='user-detail.html',
        extra_context={
            'breaks': models.Break.objects.filter(
                user__pk=pk,
                end__gte=timezone.now().date(),
            ).order_by('start')
        }
    )

    return thing_detail(handler, request, pk=pk)


@login_required
@require_http_methods(['GET', 'POST'])
def break_detail(request, pk=None):
    def pre_save(instance=None, **kwargs):
        instance.user = request.user

    handler = ThingDetailHandler(
        model_class=models.Break,
        form_class=forms.BreakForm,
        success_url=urls.reverse('user-detail', kwargs={'pk': request.user.pk}),
        pre_save=pre_save,
    )

    return thing_detail(handler, request, pk=pk)


@login_required
@require_http_methods(['GET', 'POST'])
def break_delete(request, pk):
    success_url = urls.reverse('user-detail', kwargs={'pk': request.user.pk})
    return thing_delete(models.Break, success_url, request, pk)


@login_required
@require_http_methods(['GET'])
def instrument_list(request):
    return render(request, 'instrument-list.html', context={
        'instruments': models.Instrument.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def instrument_detail(request, pk=None):
    handler = ThingDetailHandler(
        model_class=models.Instrument,
        form_class=forms.InstrumentForm,
        success_url='instrument-list',
    )
    return thing_detail(handler, request, pk=pk)


@login_required
@require_http_methods(['GET', 'POST'])
def instrument_delete(request, pk):
    return thing_delete(models.Instrument, 'instrument-list', request, pk)


@login_required
@require_http_methods(['GET', 'POST'])
def invitation_detail(request):
    handler = ThingDetailHandler(
        model_class=models.Invitation,
        form_class=forms.InvitationForm,
        success_url='invitation-list',
    )
    return thing_detail(handler, request, pk=None)


@login_required
@require_http_methods(['GET', 'POST'])
def invitation_delete(request, pk):
    return thing_delete(models.Invitation, 'invitation-list', request, pk)


@login_required
@require_http_methods(['GET'])
def song_list(request):
    return render(request, 'song-list.html', context={
        'songs': models.Song.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def song_detail(request, pk=None):
    handler = ThingDetailHandler(
        model_class=models.Song,
        form_class=forms.SongWithChartsForm,
        success_url='song-list',
    )
    return thing_detail(handler, request, pk=pk)


@login_required
@require_http_methods(['GET', 'POST'])
def song_delete(request, pk):
    return render(request, 'thing-delete.html', context={
        'thing': models.Song.objects.get(pk=pk),
    })


@login_required
@require_http_methods(['GET'])
def set_list(request):
    return render(request, 'set-list.html', context={
        'templates': models.SetTemplate.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def set_template_detail(request, pk=None):
    handler = ThingDetailHandler(
        model_class=models.SetTemplate,
        form_class=forms.SetTemplateForm,
        success_url='set-list',
    )
    return thing_detail(handler, request, pk=pk)


@login_required
@require_http_methods(['GET', 'POST'])
def set_template_delete(request, pk):
    return render(request, 'thing-delete.html', context={
        'thing': models.SetTemplate.objects.get(pk=pk),
    })
