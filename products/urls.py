from django.urls import include, path
from . import views
app_name = 'products'
urlpatterns = [
    path("products/",views.products_dashboard,name="products_dashboard"),
]