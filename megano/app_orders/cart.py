from decimal import Decimal

from app_products.models import Product
from megano import settings


class Cart(object):
    """Class Cart"""

    def __init__(self, request):
        """Initializing the cart"""

        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def add(self, product, count):
        """Adding a product to the cart, updating its quantity."""

        product_id = str(product.id)
        cart_item = self.cart.get(product_id, {"count": 0, "price": str(product.price)})
        cart_item["count"] += int(count)
        self.cart[product_id] = cart_item
        self.save()

    def save(self):
        """Saving the cart."""

        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, count):
        """
        Removing a product from the cart or reducing the quantity of a product.
        """

        product_id = str(product.id)
        if product_id in self.cart:
            if count == 1 and self.cart[product_id]["count"] > 1:
                self.cart[product_id]["count"] -= int(count)
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterating through the items in the cart and getting the products from the database.
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item["product"] = product
            cart_item["price"] = Decimal(cart_item["price"])
            cart_item["total_price"] = cart_item["price"] * cart_item["count"]
            yield cart_item

    def total_count(self):
        """Counting all products in the cart."""

        return sum(item["count"] for item in self.cart.values())

    def total_price(self):
        """Calculate the cost of products in the cart."""

        return sum(Decimal(item["price"]) * item["count"] for item in self.cart.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
