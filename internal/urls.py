from django.urls import path
from .views import api_overview , LoginView , UserView ,ShiftView

urlpatterns = [
    path('',api_overview,name='api_overview'),
    path('user-register/',UserView.as_view()),
    path('user-login/',LoginView.as_view()),
    path('add-shift/',ShiftView.as_view()),
    path('get-shift/',ShiftView.as_view())
]
