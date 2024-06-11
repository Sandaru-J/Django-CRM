from django.urls import path
from .views import UserControl,LoginView,UserView,LogoutView

urlpatterns = [
    path('user/', UserControl.as_view()),
    path('user/<int:id>/', UserControl.as_view()),
    path('login/',LoginView.as_view()),
    path('user/',UserControl.as_view()),
    path('user/<int:id>/', UserControl.as_view()),
    path('logout/',LogoutView.as_view())
]
