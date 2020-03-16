from django.urls import path

from orderapp import views

app_name = 'orderapp'

urlpatterns = [
    path('', views.to_order_view),
    path('toPay/', views.to_pay_view),
    path('checkPay/', views.check_pay_view),

]
