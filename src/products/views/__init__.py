from .index import ProductsIndexView
from .contact import ProductsContactView
from .shop import (
    ProductsShopView, ProductsCategoryView, ProductsDetailView, ProductsReviewView
)
from .search import ProductSearchView


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
    
    # search
    "ProductSearchView",
]
