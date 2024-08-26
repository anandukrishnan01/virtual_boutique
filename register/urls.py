from django.urls import path

from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('register_choice/', register_choice_view, name='register_choice'),
    path('register/customer/', customer_register_view, name='customer_register'),
    path('register/vendor/', vendor_register_view, name='vendor_register'),
    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('product_list/',product_list, name = 'product_list'),
    path('user_profile/',user_profile, name = 'user_profile'),
    

    path('product/<uuid:pk>/upload_images/', upload_images, name='upload_images'),
]
