from django.urls import path

from checkout import views


app_name = 'checkout'

urlpatterns = [
    path('shopping-cart/', views.CheckoutCartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
