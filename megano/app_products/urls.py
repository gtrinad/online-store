from django.urls import path

from .views import CategoryListAPIView, ProductListAPIView, ProductDetailAPIView, ReviewCreateAPIView, TagListAPIView, \
    LimitedEditionProductListAPIView, PopularProductListAPIView, CatalogAPIView, BannersList, SalesList

app_name = "app_products"


urlpatterns = [
    path("categories", CategoryListAPIView.as_view(), name="categories"),
    path("catalog", CatalogAPIView.as_view(), name="catalog"),
    path("banners", BannersList.as_view(), name="banners"),
    path("product", ProductListAPIView.as_view(), name="product_list"),
    path("product/<int:id>", ProductDetailAPIView.as_view(), name="product_detail"),
    path(
        "product/<int:id>/reviews",
        ReviewCreateAPIView.as_view(),
        name="product_reviews",
    ),
    path(
        "products/limited",
        LimitedEditionProductListAPIView.as_view(),
        name="products_limited",
    ),
    path(
        "products/popular", PopularProductListAPIView.as_view(), name="popular_products"
    ),
    path("tags", TagListAPIView.as_view(), name="tag_list"),
    path("sales", SalesList.as_view(), name="sales"),
]
