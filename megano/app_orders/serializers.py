from decimal import Decimal

from django.db.models import Avg
from rest_framework import serializers

from .models import Order
from app_products.models import Product
from app_products.serializers import ImageSerializer, TagSerializer, CatalogItemSerializer


class BasketSerializer(serializers.ModelSerializer):
    """Serializing a shopping cart."""

    date = serializers.DateTimeField(format="%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_count(self, obj):
        return self.context.get(str(obj.pk)).get("count")

    def get_price(self, obj):
        return Decimal(self.context.get(str(obj.pk)).get("price"))

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        average_rating = obj.reviews.aggregate(Avg("rate"))["rate__avg"]
        return round(average_rating, 2) if average_rating is not None else 0


class DateTimeTZField(serializers.DateTimeField):
    """
    A custom read-only field to handle datetime with timezone information.
    """

    def to_representation(self, value):
        if value is None:
            return None
        return value.strftime("%d.%m.%Y %H:%M")


class OrderSerializer(serializers.ModelSerializer):
    products = CatalogItemSerializer(many=True, required=True)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    createdAt = DateTimeTZField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def get_email(self, obj):
        return obj.user.user.email

    def get_fullName(self, obj):
        return obj.user.fullName

    def get_phone(self, obj):
        return obj.user.phone
