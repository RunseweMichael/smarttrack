from django.urls import path
from . import views


urlpatterns = [
    path('allcategory/', views.allcategories, name='allcategories'),
    path('createcategory/', views.createcategory, name='createcategory'),
    path('updatecategory/<int:id>', views.updatecategory, name='updatecategory'),
    path('deletecategory/<int:id>', views.deletecategory, name='deletecategory'),
    path('searchcategory/', views.searchcategory, name='searchcategory'),
]
