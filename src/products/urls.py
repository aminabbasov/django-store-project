from django.conf import settings
from django.urls import include
from django.urls import path
from django.views.decorators.cache import cache_page

from products import views


app_name = "products"

shop = [
    path("", cache_page(settings.CACHE_TTL)(views.ProductsShopView.as_view()), name="shop"),
    path(
        "category/<slug:slug>/", cache_page(settings.CACHE_TTL)(views.ProductsCategoryView.as_view()), name="category"
    ),
    path("product/<uuid:pk>/", cache_page(settings.CACHE_TTL)(views.ProductsDetailView.as_view()), name="detail"),
    path("product/<uuid:pk>/rate/", views.ProductsReviewView.as_view(), name="rate"),
    path("search/", views.ProductSearchView.as_view(), name="search"),
]

urlpatterns = [
    path("", cache_page(settings.CACHE_TTL)(views.ProductsIndexView.as_view()), name="index"),
    path("contact/", views.ProductsContactView.as_view(), name="contact"),
    path("shop/", include(shop)),
]
