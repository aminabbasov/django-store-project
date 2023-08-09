from django.contrib.postgres.search import SearchHeadline
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.contrib.postgres.search import SearchVector

from .shop import ProductsShopView


# Change to SearchVectorField, postgres trigger and GinIndex
class ProductSearchView(ProductsShopView):
    def get_queryset(self):
        query = self.request.GET.get("q") or ""
        search_vector = (
            SearchVector("name", weight="A")
            + SearchVector("short_description", weight="B")
            + SearchVector("description", weight="C")
            + SearchVector("information", weight="C")
        )
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vector, search_query)
        search_headline = SearchHeadline("name", search_query, start_sel='<b style="color: #ffc800;">', stop_sel="</b>")
        queryset = (
            super()
            .get_queryset()
            .annotate(search=search_vector, rank=search_rank, headline=search_headline)
            .filter(search=search_query, rank__gte=0.2)
        )
        order = super().get_ordering()
        return queryset.order_by("-rank") if not order else queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search_query"] = self.request.GET.get("q") or ""
        return context
