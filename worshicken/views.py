from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import auth


from db.models import Invitation, Instrument, Song, User
from . import forms


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
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=user.email, password=form.cleaned_data['password'])
            if not user:
                raise ValueError(f'could not authenticate {form.cleaned_data["email"]}')
            login(request, user)
            return redirect('home')
    else:
        form = forms.RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def user_list(request):
    return render(request, 'user-list.html', context={
        'users': User.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def user_detail(request, pk):
    if not request.user.is_superuser and request.user.pk != pk:
        return HttpResponseForbidden()

    try:
        instance = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404('User not found!')

    if request.method == 'POST':
        form = forms.UserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = forms.UserForm(None, instance=instance)

    return render(request, 'user-detail.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def instrument_list(request):
    return render(request, 'instrument-list.html', context={
        'instruments': Instrument.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def instrument_detail(request, pk=None):
    if pk:
        instance = Instrument.objects.get(pk=pk)
    else:
        instance = None

    if request.method == 'POST':
        form = forms.InstrumentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('instrument-list')
    else:
        form = forms.InstrumentForm(None, instance=instance)

    return render(request, 'instrument-detail.html', {'form': form, 'instrument': instance})


@login_required
@require_http_methods(['GET', 'POST'])
def instrument_delete(request, pk):
    if request.method == 'POST':
        Instrument.objects.get(pk=pk).delete()
        return redirect('instrument-list')
    return render(request, 'thing-delete.html', context={
        'thing': Instrument.objects.get(pk=pk),
    })


@login_required
@require_http_methods(['GET'])
def invitation_list(request):
    return render(request, 'invitation-list.html', context={
        'invitations': Invitation.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def invitation_detail(request):
    if request.method == 'POST':
        form = forms.InvitationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invitation-list')
    else:
        form = forms.InvitationForm()

    return render(request, 'invitation-detail.html', context={'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def invitation_delete(request, pk):
    instance = Invitation.objects.get(pk=pk)
    if request.method == 'POST':
        instance.delete()
        return redirect('invitation-list')
    return render(request, 'thing-delete.html', context={'thing': instance})


@login_required
@require_http_methods(['GET'])
def song_list(request):
    return render(request, 'song-list.html', context={
        'songs': Song.objects.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def song_detail(request, pk=None):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = forms.SongForm(request.POST)
        # if form.is_valid():
        #     return HttpResponseRedirect("/thanks/")
    else:
        form = forms.SongForm()
    return render(request, 'song-detail.html', context={'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def song_delete(request, pk):
    return render(request, 'thing-delete.html', context={
        'thing': Song.objects.get(pk=pk),
    })
