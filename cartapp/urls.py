from django.urls import path

from cartapp import views

app_name = 'cartapp'

urlpatterns = [
    path('', views.CartView.as_view()),
    path('queryAll/', views.CartListView.as_view()),
]
