from django.db.models import Avg
from rest_framework import serializers

from .models import (
    CategoryIcon,
    Category,
    ProductImage,
    Review,
    Tag,
    Product,
    SpecificationValue,
    Sale,
)


class CategoryIconSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = CategoryIcon
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryIconSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]

    def get_subcategories(self, obj):
        if obj.parent is None:
            subcategories = obj.subcategories.all()
            if subcategories:
                serializer = self.__class__(subcategories, many=True)
                return serializer.data
            return []


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Review
        fields = ["text", "author", "email", "rate", "date"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    images = ImageSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            average_rating = round(reviews.aggregate(Avg("rate"))["rate__avg"], 2)
            return average_rating or 0
        return 0

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_specifications(self, obj):
        specifications = SpecificationValue.objects.filter(product=obj)
        return [
            {"name": specification.specification.name, "value": specification.value}
            for specification in specifications
        ]


class LimitedProductSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%a %b %d %Y %H:%M:%S GMT%z (%Z)")
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

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            average_rating = round(reviews.aggregate(Avg("rate"))["rate__avg"], 2)
            return average_rating or 0
        return 0


class CatalogItemSerializer(serializers.ModelSerializer):
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

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            average_rating = round(reviews.aggregate(Avg("rate"))["rate__avg"], 2)
            return average_rating or 0
        return 0


class SaleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id")
    dateFrom = serializers.DateField(format="%d-%m")
    dateTo = serializers.DateField(format="%d-%m")
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    images = ImageSerializer(source="product.images", many=True)

    class Meta:
        model = Sale
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]

    def get_price(self, obj):
        return obj.product.price

    def get_title(self, obj):
        return obj.product.title
