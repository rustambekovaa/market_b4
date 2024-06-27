from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('products/', views.list_create_products),
    path('products/<int:id>/', views.detail_update_delete_products),
    path('category/', views.create_category),
    path('category/<int:id>/', views.detail_category),
    path('tag/', views.create_tag),
    path('tag/<int:id>/', views.detail_tag),
    path('auth/', include('api.auth.urls'))
]