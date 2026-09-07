from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListCreateAPIView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        category = serializer.save()

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )


class ProductListCreateAPIView(APIView):

    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.save()
        cache.clear()
        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )