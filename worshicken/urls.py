from django.urls import path
from django.contrib.auth import views as auth_views

from worshicken import views


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('register/', views.Register.as_view(), name="register"),
    path('invitations/', views.Invitations.as_view(), name="invitations"),
    path('invitations/new', views.InvitationCreate.as_view(), name="invitation-create"),
    path('invitations/<uuid:pk>', views.InvitationDelete.as_view(), name="invitation-delete"),
    path('', views.Home.as_view(), name="home"),
]
