from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/<int:id>/', views.DetailUpdateDeleteProductAPiView.as_view()),
    path('category/', views.ListCreateCategoryApiView.as_view()),
    path('category/<int:id>/', views.DetailUpdateDeleteCategoryApiView.as_view()),
    path('tag/', views.ListCreateCategoryApiView.as_view()),
    path('tag/<int:id>/', views.DetailUpdateDeleteTagApiView.as_view()),
    path('auth/', include('api.auth.urls'))
]