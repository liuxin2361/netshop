from django.urls import path

from orderapp import views

app_name = 'orderapp'

urlpatterns = [
    path('', views.to_order_view),
]
