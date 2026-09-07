from django.db.models import Q, IntegerField,Case, When

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from products.models import Product
from .serializers import ProductSearchSerializer


class ProductSearchAPIView(APIView):

    def get(self, request):
        cache_key = f"product_search:{request.get_full_path()}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        keyword = request.GET.get("q")
        category = request.GET.get("category")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        store_id = request.GET.get("store_id")
        in_stock = request.GET.get("in_stock")
        sort = request.GET.get("sort")

        products = Product.objects.select_related("category")

        if keyword:
            products = products.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(category__name__icontains=keyword))

        if category:
            products = products.filter(category_id=category)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        if store_id:
            products = products.filter(
                inventory__store_id=store_id)

        if in_stock == "true":
            products = products.filter(
                inventory__quantity__gt=0)

        if sort == "price":
            products = products.order_by("price")

        elif sort == "newest":
            products = products.order_by("-created_at")

        else:
            products = products.order_by("-id")

        products = products.distinct()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        page = paginator.paginate_queryset(products, request)

        serializer = ProductSearchSerializer(page,many=True)

        response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key,response.data, 60 * 5)
        return response


class ProductSuggestAPIView(APIView):

    def get(self, request):
        query = request.GET.get("q", "").strip()

        if len(query) < 3:
            return Response({
                "error": "q must contain at least 3 characters."
            }, status=400)

        products = (
            Product.objects.filter(title__icontains=query).annotate(priority=Case(When(title__istartswith=query, then=1),default=2,output_field=IntegerField())).order_by("priority", "title").values_list("title", flat=True)[:10])

        return Response({
            "results": list(products)})