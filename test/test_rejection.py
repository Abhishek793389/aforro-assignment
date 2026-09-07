from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Category, Product
from stores.models import Store, Inventory


class OrderRejectionTest(TestCase):

    def test_insufficient_stock(self):
        client = APIClient()

        category = Category.objects.create(name="Books")
        product = Product.objects.create(
            title="Book",
            price=500,
            category=category
        )
        store = Store.objects.create(
            name="Store 1",
            location="Delhi"
        )
        Inventory.objects.create(
            store=store,
            product=product,
            quantity=2
        )

        response = client.post(
            "/api/orders/",
            {
                "store_id": store.id,
                "items": [
                    {
                        "product_id": product.id,
                        "quantity_requested": 5
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(response.data["status"], "REJECTED")