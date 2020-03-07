from django.urls import path

from goodsapp import views

app_name = 'goodsapp'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('category/<int:category_id>/', views.IndexView.as_view()),
    path('category/<int:category_id>/page/<int:page>/', views.IndexView.as_view()),
]
