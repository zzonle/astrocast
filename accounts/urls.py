from django.urls import path
from .views import RegisterView, UserMeView, UserProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserMeView.as_view(), name='user_me'),
    path('profile/', UserProfileUpdateView.as_view(), name='user_profile_update'),
]