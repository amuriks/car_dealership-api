from django.urls import path

from .views import UserProfileView

urlpatterns = [
    path('<pk>/', UserProfileView.as_view()),
]
