from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Store,Inventory
from .serializers import StoreSerializer,InventorySerializer
from django.db.models import Count
from orders.models import Order
from orders.serializers import OrderListSerializer
from drf_spectacular.utils import extend_schema


class StoreListCreateAPIView(APIView):

    def get(self, request):
        stores = Store.objects.all()

        serializer = StoreSerializer(stores,many=True)

        return Response(serializer.data)

    @extend_schema(
    request=StoreSerializer,
    responses=StoreSerializer)
    def post(self, request):
        serializer = StoreSerializer(data=request.data)

        if serializer.is_valid():
            store = serializer.save()

            return Response(
                StoreSerializer(store).data,
                status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

class StoreInventoryAPIView(APIView):

    def get(self, request, store_id):

        if not Store.objects.filter(id=store_id).exists():
            return Response(
                {"error": "Store not found."},
                status=status.HTTP_404_NOT_FOUND)

        inventory = (Inventory.objects.filter(store_id=store_id).select_related("product", "product__category").order_by("product__title"))
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

class StoreOrdersAPIView(APIView):

    def get(self, request, store_id):

        if not Store.objects.filter(id=store_id).exists():
            return Response(
                {"error": "Store not found."},
                status=status.HTTP_404_NOT_FOUND)

        orders = (Order.objects.filter(store_id=store_id).annotate(total_items=Count("items")).order_by("-created_at"))
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)