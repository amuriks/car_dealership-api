from django.urls import path, include

from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('signin/', UserLoginView.as_view()),
    path('profile/', include('apps.user_profile.urls')),
]
