from django.urls import path
from .views import NumberAPIView

urlpatterns = [
     path('numbers/<str:numberid>/', NumberAPIView.as_view(), name='number-api'),
]
