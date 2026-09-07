from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_order_confirmation
from stores.models import Store, Inventory
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderCreateAPIView(APIView):

    def post(self, request):
        store_id = request.data.get("store_id")
        items = request.data.get("items")

        if not store_id:
            return Response(
                {"error": "store_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(items, list) or not items:
            return Response(
                {"error": "items must be a non-empty list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(
            data={
                "store": store_id,
                "items": items,
            }
        )

        

        serializer.is_valid(raise_exception=True)

        validated_items = serializer.validated_data["items"]



        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response(
                {"error": "Store not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        with transaction.atomic():

            order = Order.objects.create(
                store=store,
                status=Order.Status.PENDING
            )

            rejected = False
            inventory_rows = {}

            for item in validated_items:

                product_id = item["product_id"]
                quantity_requested = item["quantity_requested"]

                try:
                    inventory = (
                        Inventory.objects
                        .select_for_update()
                        .get(
                            store_id=store_id,
                            product_id=product_id
                        )
                    )
                except Inventory.DoesNotExist:
                    rejected = True
                    continue

                inventory_rows[product_id] = inventory

                if inventory.quantity < quantity_requested:
                    rejected = True

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product_id=item["product_id"],
                    quantity_requested=item["quantity_requested"]
                )
                for item in validated_items
            ])

            if rejected:
                order.status = Order.Status.REJECTED
                order.save(update_fields=["status"])

            else:
                for item in validated_items:
                    inventory = inventory_rows[item["product_id"]]
                    inventory.quantity -= item["quantity_requested"]
                    inventory.save(update_fields=["quantity"])

                order.status = Order.Status.CONFIRMED
                order.save(update_fields=["status"])
                transaction.on_commit(
                lambda: send_order_confirmation.delay(order.id))

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )