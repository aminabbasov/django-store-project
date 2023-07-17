from .index import ProductsIndexView
from .contact import ProductsContactView
from .shop import (
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
