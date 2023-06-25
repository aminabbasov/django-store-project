from products.views.index import ProductsIndexView
from products.views.contact import ProductsContactView
from products.views.shop import (
    ProductsShopView, ProductsCategoryView, ProductsDetailView, ProductsReviewView
)


__all__ = [
    # index
    "ProductsIndexView",
    
    # contact
    "ProductsContactView",
    
    # shop
    "ProductsShopView",
    "ProductsCategoryView",
    "ProductsDetailView",
    "ProductsReviewView",
]
