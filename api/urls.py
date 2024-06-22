from . import views
from django.urls import path


urlpatterns = [
    path('products/', views.list_products),
    path('products/<int:id>/', views.detail_products),
    path('category/', views.create_category),
    path('category/<int:id>/', views.detail_category),
    path('tag/', views.create_tag),
    path('tag/<int:id>/', views.detail_tag),
]