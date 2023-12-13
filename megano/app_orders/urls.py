from django.urls import path

from .views import BasketOfProductsView, Orders, OrderDetail, PaymentView

app_name = "app_orders"


urlpatterns = [
    path("orders", Orders.as_view()),
    path("order/<int:pk>", OrderDetail.as_view()),
    path("payment/<int:pk>", PaymentView.as_view()),
    path("basket", BasketOfProductsView.as_view(), name="basket"),
]
