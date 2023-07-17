from django.urls import path

from checkout import views


app_name = 'checkout'

urlpatterns = [
    path('basket/', views.CheckoutBasketView.as_view(), name='basket'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
