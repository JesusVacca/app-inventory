from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),

    path('inventory-input/', views.InputMovementView.as_view(), name='inventory-input'),
    path('inventory-output/', views.OutputMovementView.as_view(), name='inventory-output'),
    path('inventory-input/create/', views.CreateInputMovementView.as_view(), name='inventory-input-create'),
    path('inventory-output/create/', views.CreateOutputMovementView.as_view(), name='inventory-output-create'),

]