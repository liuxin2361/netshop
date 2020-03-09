from django.urls import path

from userapp import views

app_name = 'userapp'

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('center/', views.center_view),
    path('login/', views.LoginView.as_view()),
    path('loadCode/', views.LoadCodeView.as_view()),
    path('checkCode/', views.CheckCodeView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
