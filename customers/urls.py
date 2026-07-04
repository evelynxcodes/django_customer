from django.urls import path

from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_create, name='customer_create'),
    path('<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('export/customers.zip', views.export_customers_zip, name='export_customers_zip'),
    path('export/project.zip', views.download_project_zip, name='download_project_zip'),
]
