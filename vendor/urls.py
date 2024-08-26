from django.urls import path

from .views import *

urlpatterns = [
    path('vendor_dashboard/',vendor,name="vendordashboard"),
    path('profile/', vendor_profile_view, name='vendor_profile'),


    path('addbrand/',addbrand,name="addbrand"),
    path('savedata/',savedata,name="savedata"),
    path('displaybrand/',displaybrand,name="displaybrand"),
    path('editbrand/<uuid:dataid>/',editbrand,name="editbrand"),
    path('updatebrand/<uuid:dataid>/',updatebrand,name="updatebrand"),
    path('deletebrand/<uuid:dataid>/',deletebrand,name="deletebrand"),
    
    path('manage_categories/', manage_categories, name='manage_categories'),
    path('savedata1/', savedata1, name='savedata1'),
    path('updatecategory/<uuid:dataid>/', updatecategory, name='updatecategory'),
    path('deletecategory/<uuid:dataid>/', deletecategory, name='deletecategory'),

    path('displayproduct/', product_list, name='displayproduct'),
    path('add/', add_product, name='add_product'),
    path('edit/<uuid:pk>/', edit_product, name='edit_product'),
    path('delete/<uuid:dataid>/', deleteproduct, name='delete_product'),
    path('ajax/filter_categories/', filter_categories, name='filter_categories'),

    path('manage_product_sizes/', manage_product_sizes, name='manage_product_sizes'),
    path('save_product_size/', save_product_size, name='save_product_size'),
    path('update_product_size/<uuid:dataid>/', update_product_size, name='update_product_size'),
    path('delete_product_size/<uuid:dataid>/', delete_product_size, name='delete_product_size'),

    path('product_alternatives/', product_alternatives, name='product_alternatives'),
    path('product_alternatives/edit/<uuid:dataid>/', edit_product_alternative, name='edit_product_alternative'),
    path('product_alternatives/delete/<uuid:dataid>/', delete_product_alternative, name='delete_product_alternative'),

    path('product_list/<uuid:product_id>/', product_detail, name='product_detail'),
    path('get_alternative_selling_price/', get_alternative_selling_price, name='get_alternative_selling_price'),

    path('product_list/<uuid:product_id>/add_to_cart/<uuid:dataid>/', add_to_cart, name='add_to_cart'),
    path('display_cart_item/', display_cart_item, name='display_cart_item'),
    path('update_cart_item/<uuid:item_id>/<str:action>/', update_cart_item, name='update_cart_item'),
    path('remove_cart_item/<uuid:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('checkout_page/', checkout_page, name='checkout_page'),
    path('payment_success/', payment_success, name='payment_success'),

     # address
    path('add_address/', add_address, name='add_address'),
    path('edit_address/<uuid:address_id>/', edit_address, name='edit_address'),
    path('delete_address/<uuid:address_id>/', delete_address, name='delete_address'),
    path('select_address/<uuid:address_id>/', select_address, name='select_address'),
]
