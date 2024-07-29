from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

from worshicken import views


urlpatterns = [
    # auth
    path('auth/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('auth/register/', views.register, name='register'),
    path('auth/logout/', views.logout, name='logout'),

    # members
    path('members/', views.user_list, name='user-list'),
    path('members/<uuid:pk>', views.user_detail, name='user-detail'),

    # breaks
    path('breaks/new', views.break_detail, name='break-new'),
    path('breaks/<uuid:pk>/delete', views.break_delete, name='break-delete'),

    # invitations
    path('invitations/new', views.invitation_detail, name='invitation-detail'),
    path('invitations/<uuid:pk>', views.invitation_detail, name='invitation-detail'),
    path('invitations/<uuid:pk>/delete', views.invitation_delete, name='invitation-delete'),

    # songs/
    path('songs/', views.song_list, name='song-list'),
    path('songs/new', views.song_detail, name='song-new'),
    path('songs/<uuid:pk>', views.song_detail, name='song-detail'),
    path('songs/<uuid:pk>/delete', views.song_delete, name='song-delete'),

    # instruments/
    path('instruments/', views.instrument_list, name='instrument-list'),
    path('instruments/new', views.instrument_detail, name='instrument-new'),
    path('instruments/<uuid:pk>', views.instrument_detail, name='instrument-detail'),
    path('instruments/<uuid:pk>/delete', views.instrument_delete, name='instrument-delete'),

    # sets/
    path('sets/', views.set_list, name='set-list'),
    path('sets/templates/new', views.set_template_detail, name='set-template-new'),
    path('sets/templates/<uuid:pk>', views.set_template_detail, name='set-template-detail'),
    path('sets/templates/<uuid:pk>/delete', views.set_template_delete, name='set-template-delete'),

    # home
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
