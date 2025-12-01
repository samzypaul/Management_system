from django.urls import include, path
from . import views
app_name = 'products'
urlpatterns = [
    path("products/",views.products_dashboard,name="products_dashboard"),
    path("products/addproduct/",views.add_product,name="add_product"),
    path("products/updateproduct/<str:pk>/",views.update_product,name="update_product"),
    path("updateproduct/updateproduct_record/<str:pk>",views.update_product_record,name="update_product_record"),
    path("products/deleteproduct/<str:pk>",views.delete_product,name="delete_product"),

]