from django.urls import path
from . import views
app_name = 'User'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about_us'),
    path('login/',views.login_page, name='login'),
]