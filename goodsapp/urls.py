from django.urls import path

from goodsapp import views

app_name = 'goodsapp'

urlpatterns = [
    path('', views.IndexView.as_view())
]
