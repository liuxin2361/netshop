from django.urls import path

from userapp import views

app_name = 'userapp'

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('center/', views.center_view),
]