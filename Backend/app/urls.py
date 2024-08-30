from django.urls import path
from .views import UserControl,ProductControl,LoginView,OrderControl,StockControl

urlpatterns = [
    path('user/', UserControl.as_view()),
    path('user/<int:id>/', UserControl.as_view()),
    path('user/<str:email>/', UserControl.as_view()),

    path('login/',LoginView.as_view()),

    path('product/', ProductControl.as_view()),
    path('product/<int:id>/', ProductControl.as_view()),

    path('order/', OrderControl.as_view()),
    path('order/<int:id>/', OrderControl.as_view()),

    path('stock/', StockControl.as_view()),
    path('stock/<int:id>/', StockControl.as_view())
]