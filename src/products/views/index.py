from typing import Any

from django.views import generic

from products.models import Category
from products.models import SingleProductView


class ProductsIndexView(generic.TemplateView):
    template_name = "products/index.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["carousel"] = Category.objects.manual_order(["man", "woman", "baby"])
        context["main_discount"] = SingleProductView.objects.highest_discount()[:2]
        context["second_discount"] = SingleProductView.objects.newest_discount()[:2]
        context["categories"] = Category.objects.annotate_product_count()
        context["featured_products"] = SingleProductView.objects.all()[:4]
        context["recent_products"] = SingleProductView.objects.newest()[:4]

        return context
