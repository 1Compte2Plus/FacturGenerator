from django.urls import path
from . import views

app_name = 'main'  # Namespace pour l'application

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice-list'),
    path('invoice/add/', views.InvoiceCreateView.as_view(), name='invoice-add'),
    path('invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice-delete'),
]