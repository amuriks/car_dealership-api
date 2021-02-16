from django.urls import path

from .views import CarView, CarListView

urlpatterns = [
    path('', CarListView.as_view()),
    path('<pk>/', CarView.as_view()),
]
