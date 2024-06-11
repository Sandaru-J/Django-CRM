from django.urls import path
from .views import ProductControl

urlpatterns = [
    path('product/',ProductControl.as_view()),
    path('product/<int:id>/',ProductControl.as_view())
]
