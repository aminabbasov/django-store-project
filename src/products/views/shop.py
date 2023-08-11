from typing import Any, Literal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import QuerySet
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic

from products.forms import ProductsReviewForm
from products.models import Category
from products.models import Product
from products.models import ProductOption
from products.models import ProductView
from products.models import SingleProductView


class ProductsShopView(generic.ListView):
    model = SingleProductView
    context_object_name = "products"
    template_name = "products/shop.html"
    paginate_by = 3

    def get_paginate_by(self, queryset: QuerySet) -> int:
        self.paginate_by = self.request.GET.get("paginate_by", self.paginate_by)  # example: ?paginate_by3&page=2
        return int(self.paginate_by)

    def paginate_queryset(self, queryset: QuerySet[SingleProductView], page_size: int) -> tuple:
        paginator = Paginator(queryset, page_size)
        try:
            return super().paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs["page"] = paginator.num_pages
            return super().paginate_queryset(queryset, page_size)

    def get_queryset(self) -> QuerySet[SingleProductView]:
        queryset = SingleProductView.objects.all()

        # order
        ordering = self.get_ordering()
        if ordering and isinstance(ordering, str):
            ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        elif ordering and isinstance(ordering, list):
            queryset = queryset.manual_order(ordering)

        # filter by price
        price_filter = self._get_price_query()
        queryset = queryset.filter(price_filter)

        # filter by options (in fact only by color and size)
        options_filter_list = [
            self.request.GET.getlist("color_filter"),
            self.request.GET.getlist("size_filter"),
        ]

        filter_q = Q()
        for options_filter in options_filter_list:
            filter_q &= self._get_options_query(options_filter)

        options = ProductOption.objects.filter(filter_q)
        product_ids = [item.product.id for item in options]

        return queryset.filter(product_id__in=product_ids)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["paginate_by"] = self.paginate_by
        context["selected_price"] = self.request.GET.getlist("price_filter")
        context["selected_color"] = self.request.GET.getlist("color_filter")
        context["selected_size"] = self.request.GET.getlist("size_filter")

        return context

    def get_ordering(self) -> Literal["-created", "views"] | list[int] | None:
        ordering = self.request.GET.get("sort")

        if ordering == "latest":
            return "-created"
        elif ordering == "popularity":
            return "views"
        elif ordering == "rating":
            products = Product.objects.average_rating()
            products = products.order_by("-avg_rating")
            return [item.id for item in products]

        return ordering

    def _get_options_query(self, options_filter: list) -> Q:
        """Method for ProductOption."""
        option_q = Q()

        for option in options_filter:
            if option:
                option_q |= Q(values__overlap=[option])

        return option_q

    def _get_price_query(self) -> Q:
        """Method for SingleProductView.

        Example:

                $80____________$160
        $0 ---------- $100 ---------- $200

        This product will be in 2 range filters.
        """
        price_values = {
            "1-100": {"max_discounted_price__gte": 0.01, "min_discounted_price__lte": 100},
            "100-200": {"max_discounted_price__gte": 101.01, "min_discounted_price__lte": 200},
            "200-300": {"max_discounted_price__gte": 201.01, "min_discounted_price__lte": 300},
            "300-400": {"max_discounted_price__gte": 301.01, "min_discounted_price__lte": 400},
            "400+": {"max_discounted_price__gte": 401.01},
        }

        price_q = Q()

        for price in self.request.GET.getlist("price_filter"):
            if price:
                price_q |= Q(**price_values[price])

        return price_q


class ProductsCategoryView(ProductsShopView):
    def get_queryset(self) -> QuerySet[SingleProductView]:
        queryset = super().get_queryset()
        slug = self.kwargs.get("slug")
        return queryset.by_category(slug=slug)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get("slug")

        return context


class ProductsDetailView(generic.DetailView):
    model = SingleProductView
    template_name = "products/detail.html"
    context_object_name = "product"

    def get_object(self) -> SingleProductView:
        public_id = self.kwargs.get(self.pk_url_kwarg)
        return self.model.objects.get(public_id=public_id)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["related_products"] = self.model.objects.related_products(
            categories=Category.objects.all(), exclude_model=self.get_object()
        )[:5]
        context["review_form"] = ProductsReviewForm(instance=self.get_object())

        return context

    def post(self, *args: Any, **kwargs: dict[str, Any]) -> HttpResponseRedirect:
        if not (quantity := int(self.request.POST["quantity"])):
            messages.error(self.request, "Can't add less than one product.")
            return redirect("products:detail", pk=self.kwargs["pk"])

        try:
            product = get_object_or_404(
                ProductView.objects.filter(
                    public_id=(public_id := str(self.kwargs["pk"])),
                ).by_options(
                    color=(color := str(self.request.POST.get("color"))),
                    size=(size := str(self.request.POST.get("size"))),
                )
            )
            price = str(product.price)
            variant_id = int(product.variant_id)

        except Http404:
            messages.error(self.request, "Sorry, this product is out of stock.")
            return redirect("products:detail", pk=self.kwargs["pk"])

        try:
            self.request.basket.add(
                variant_id=variant_id, quantity=quantity, price=price, option={"size": size, "color": color}
            )
            messages.success(self.request, "Product added to basket.")

        except MultiValueDictKeyError:
            messages.error(self.request, "Please select an options.")

        except Exception:  # noqa: PIE786
            messages.error(self.request, "Something went wrong, please try again later.")

        return redirect("products:detail", pk=public_id)


class ProductsReviewView(LoginRequiredMixin, generic.FormView):
    template_name = "products/detail.html"
    http_method_names = ["post"]
    form_class = ProductsReviewForm

    def get_success_url(self) -> str:
        return reverse_lazy("products:detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form: ProductsReviewForm) -> HttpResponse:
        review = form.save(commit=False)
        review.product_id = SingleProductView.objects.get(
            public_id=self.kwargs["pk"]
        ).product_id  # because ForeingKey is for id, but pk gives uuid
        review.user_id = self.request.user.pk
        review.save()
        messages.success(self.request, "You left a comment. Thank you!")

        return super(ProductsReviewView, self).form_valid(form)

    def form_invalid(self, form: ProductsReviewForm) -> HttpResponse:
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)

        return redirect("products:detail", pk=self.kwargs["pk"])
