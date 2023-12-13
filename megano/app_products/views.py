from typing import Any, Dict

from django.db.models import Count, Avg
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Tag, Sale
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, TagSerializer, \
    LimitedProductSerializer, CatalogItemSerializer, SaleSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(parent=None, is_active=True)
    serializer_class = CategorySerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = "id"


class ReviewCreateAPIView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        product_id = self.kwargs.get("id")
        product = Product.objects.get(pk=product_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagListAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class LimitedEditionProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(limited_edition=True)[:16]
    serializer_class = LimitedProductSerializer


class PopularProductListAPIView(ListAPIView):
    serializer_class = LimitedProductSerializer

    def get_queryset(self):
        queryset = Product.objects.annotate(review_count=Count("reviews")).order_by(
            "-review_count", "-count"
        )[:8]
        return queryset


class CatalogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)


class CatalogAPIView(ListAPIView):
    serializer_class: Any = CatalogItemSerializer
    pagination_class: Any = CatalogPagination

    def get_queryset(self) -> Any:
        queryset: Any = Product.objects.filter(is_active=True)

        # Apply filters
        filters: Dict[str, Any] = self.request.query_params

        name: str = filters.get("filter[name]")
        min_price: float = filters.get("filter[minPrice]")
        max_price: float = filters.get("filter[maxPrice]")
        free_delivery = filters.get("filter[freeDelivery]") == "true"
        available = filters.get("filter[available]") == "true"

        if name:
            queryset = queryset.filter(title__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if free_delivery:
            queryset = queryset.filter(freeDelivery=True)
        if available:
            queryset = queryset.filter(count__gt=0)

        # Apply tag filter
        tags = self.request.query_params.getlist("tags[]")
        if tags:
            queryset = queryset.filter(tags__in=tags)

        # Apply sorting
        sort: str = self.request.query_params.get("sort", "date")
        sort_type: str = self.request.query_params.get("sortType", "dec")

        if sort == "price":
            queryset = queryset.order_by(f'{"" if sort_type == "dec" else "-"}price')
        elif sort == "reviews":
            queryset = queryset.annotate(reviews_count=Count("reviews")).order_by(
                f'{"" if sort_type == "dec" else "-"}reviews_count'
            )
        elif sort == "rating":
            queryset = queryset.annotate(rating_avg=Avg("reviews__rate")).order_by(
                f'{"" if sort_type == "dec" else "-"}rating_avg'
            )
        else:
            queryset = queryset.order_by(f'{"" if sort_type == "dec" else "-"}date')

        return queryset

    def list(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        queryset: Any = self.filter_queryset(self.get_queryset())
        page: Any = self.paginate_queryset(queryset)
        serializer: Any = self.get_serializer(page, many=True)

        data: Dict[str, Any] = {
            "items": serializer.data,
            "currentPage": self.paginator.page.number,
            "lastPage": self.paginator.page.paginator.num_pages,
        }
        return self.get_paginated_response(data)


class BannersList(APIView):
    def get(self, request: Request) -> Response:
        favourite_categories = [
            obj.pk for obj in Category.objects.filter(favourite=True)
        ]
        banners = Product.objects.filter(category_id__in=favourite_categories)

        serialized = LimitedProductSerializer(banners, many=True)
        return Response(serialized.data)


class SalesPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100


class SalesList(APIView):
    pagination_class = SalesPagination

    def get(self, request: Request) -> Response:
        current_page = int(request.query_params.get("currentPage", 1))

        items = Sale.objects.all().order_by("id")
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request)

        serializer = SaleSerializer(paginated_items, many=True)

        data = {
            "items": serializer.data,
            "currentPage": current_page,
            "lastPage": paginator.page.paginator.num_pages,
        }

        return Response(data)
