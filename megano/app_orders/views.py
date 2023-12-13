from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart
from .models import Order, ProductsInOrder
from .serializers import BasketSerializer, OrderSerializer
from app_products.models import Product


class BasketOfProductsView(APIView):
    """
    View to get and remove products from cart, and add products to cart.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        cart = Cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        cart = Cart(request)
        product = get_object_or_404(Product, id=request.data.get("id"))
        count = int(request.data.get("count"))
        cart.add(product=product, count=count)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        cart = Cart(request)
        product = get_object_or_404(Product, id=request.data.get("id"))
        count = request.data.get("count", None)
        cart.remove(product, count=count)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def get_serializer(self, cart):
        """Retrieving products from the cart."""

        products_in_cart = [product for product in cart.cart.keys()]
        products = Product.objects.filter(pk__in=products_in_cart)
        return BasketSerializer(products, many=True, context=cart.cart)


class Orders(APIView):
    def get(self, request: Request) -> Response:
        data = Order.objects.filter(user_id=request.user.profile.pk)
        serialized = OrderSerializer(data, many=True)
        return Response(serialized.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        products_in_order = [
            (obj["id"], obj["count"], obj["price"]) for obj in request.data
        ]
        print("products_in_order", products_in_order)
        product_ids = list(zip(*products_in_order))[0]
        print("product_ids", product_ids)

        with transaction.atomic():
            cart = Cart(request)
            print("cart")

            order, created = Order.objects.get_or_create(
                user=request.user.profile,
                totalCost=cart.total_price(),
            )

            if not created:
                # Если заказ уже существует, убедимся, что он не содержит другие продукты
                order.products.clear()

            products = Product.objects.filter(id__in=product_ids)
            print("products", products)
            order.products.set(products)

        data = {"orderId": order.pk}
        return Response(data)


class OrderDetail(APIView):
    def get(self, request: Request, pk) -> Response:
        order = get_object_or_404(Order, pk=pk)
        serialized = OrderSerializer(order)
        cart = Cart(request).cart
        data = serialized.data

        try:
            products_in_order = data["products"]
            query = ProductsInOrder.objects.filter(order_id=pk)
            prods = {obj.product.pk: obj.count for obj in query}
            for prod in products_in_order:
                prod["count"] = prods[prod["id"]]
        except:
            products_in_order = data["products"]
            for prod in products_in_order:
                prod["count"] = cart[str(prod["id"])]["count"]

        return Response(data)

    def post(self, request: Request, pk) -> Response:
        order = get_object_or_404(Order, pk=pk)
        data = request.data
        order.fullName = data["fullName"]
        order.phone = data["phone"]
        order.email = data["email"]
        order.deliveryType = data["deliveryType"]
        order.city = data["city"]
        order.address = data["address"]
        order.paymentType = data["paymentType"]
        order.status = "Awaiting payment"

        if data["deliveryType"] == "express":
            order.totalCost += 500
        elif order.totalCost < 2000:
            order.totalCost += 200

        order.save()

        for product in data["products"]:
            product_id = product["id"]
            count = product["count"]

            ProductsInOrder.objects.get_or_create(
                order_id=order.pk, product_id=product_id, count=count
            )

        Cart(request).clear()
        return Response(request.data, status=status.HTTP_201_CREATED)


class PaymentView(APIView):
    def post(self, request: Request, pk) -> Response:
        order = get_object_or_404(Order, pk=pk)
        order.status = "Paid"
        order.save()
        return Response(request.data, status=status.HTTP_200_OK)
