from django.urls import path, include

from products import views


app_name = 'products'

shop = [
    path('', views.ProductsShopView.as_view(), name='shop'),
    path('category/<slug:slug>/', views.ProductsCategoryView.as_view(), name='category'),
    path('product/<int:pk>/', views.ProductsDetailView.as_view(), name='detail'),
    path('product/<int:pk>/rate/', views.ProductsReviewView.as_view(), name='rate'),
]

urlpatterns = [
    path('', views.ProductsIndexView.as_view(), name='index'),
    path('contact/', views.ProductsContactView.as_view(), name='contact'),
    path('shop/', include(shop)),
]
