from django.urls import path
from django.contrib.auth.views import LoginView

from worshicken import views

# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']


urlpatterns = [
    # auth
    path('auth/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('auth/register/', views.register, name='register'),
    path('auth/logout/', views.logout, name='logout'),

    # members
    path('members/', views.user_list, name='user-list'),
    path('members/<uuid:pk>', views.user_detail, name='user-detail'),

    # invitations
    path('invitations/', views.invitation_list, name='invitation-list'),
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

    # home
    path('', views.home, name='home'),
]
