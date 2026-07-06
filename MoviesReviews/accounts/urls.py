from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import BootstrapAuthenticationForm

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=BootstrapAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/my-reviews/', views.MyReviewsView.as_view(), name='my_reviews'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
]