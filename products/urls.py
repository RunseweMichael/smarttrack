from django.urls import path
from . import views
from .views import ProductDetailView

urlpatterns = [
    path('products_list/', views.products_list, name='products_list'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>', views.delete, name='deleteproduct'),
    path('update/<int:id>', views.update, name='updateproduct'),
    path('update/<int:id>', views.update, name='updateproduct'),
    path('viewproduct/<int:pk>', ProductDetailView.as_view(), name='viewproduct'),
    path('export/', views.export, name='export'),
]
