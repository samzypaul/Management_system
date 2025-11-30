from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path("orders/",views.orders_dashboard,name="orders_dashboard"),
    path("orders/orders_list/",views.orders_details,name="orders_details"),
]