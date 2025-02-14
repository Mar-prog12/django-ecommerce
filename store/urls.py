from django.urls import path
from .views import product_list, search_products, view_cart, add_to_cart, remove_from_cart, clear_cart,  contact_page


urlpatterns = [
    path('', product_list, name='product_list'),
    path('search/', search_products, name='search_products'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('contact/', contact_page, name='contact_page'),
]

