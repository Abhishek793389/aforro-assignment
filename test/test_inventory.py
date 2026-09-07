from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Category, Product
from stores.models import Store, Inventory


class InventoryTest(TestCase):

    def test_inventory(self):
        client = APIClient()

        category = Category.objects.create(name="Shoes")
        product = Product.objects.create(
            title="Running Shoes",
            price=2000,
            category=category)
        store = Store.objects.create(
            name="Store 1",
            location="Delhi")
        Inventory.objects.create(store=store,product=product,quantity=20)

        response = client.get(f"/api/stores/{store.id}/inventory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["quantity"], 20)