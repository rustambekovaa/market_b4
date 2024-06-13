from . import views
from django.urls import path


urlpatterns = [
    path('products/', views.list_products),
    path('products/<int:id>/', views.detail_products),
]