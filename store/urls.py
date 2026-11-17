
from django.urls import path
from . import views

urlpatterns = [

    # Homepage
    path('', views.home_view, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buyer/orders/', views.buyer_orders, name='buyer_orders'),
    # Buyer dashboard
    path(
        'buyer/dashboard/',
        views.buyer_dashboard,
        name='buyer_dashboard'
    ),

    # Seller dashboard
    path(
        'seller/dashboard/',
        views.seller_dashboard,
        name='seller_dashboard'
    ),


    path(
    'seller/products/',
    views.seller_products,
    name='seller_products'
),

path(
    'seller/products/add/',
    views.add_product,
    name='add_product'
),

path(
    'seller/products/edit/<int:product_id>/',
    views.edit_product,
    name='edit_product'
),

path(
    'seller/products/delete/<int:product_id>/',
    views.delete_product,
    name='delete_product'
),

# ==========================================
# BUYER: SHOPPING CART
# ==========================================

path(
    'buyer/cart/',
    views.cart_view,
    name='cart'
),

path(
    'buyer/cart/add/<int:product_id>/',
    views.add_to_cart,
    name='add_to_cart'
),

path(
    'buyer/cart/update/<int:product_id>/',
    views.update_cart,
    name='update_cart'
),

path(
    'buyer/cart/remove/<int:product_id>/',
    views.remove_from_cart,
    name='remove_from_cart'
),

path('buyer/checkout/', views.checkout_view, name='checkout'),

path('buyer/place-order/', views.place_order, name='place_order'),

path(
    'buyer/order-success/<int:order_id>/',
    views.order_success,
    name='order_success'
),


path(
    'seller/orders/',
    views.seller_orders,
    name='seller_orders'
),

path(
    'seller/orders/update/<int:item_id>/',
    views.update_order_status,
    name='update_order_status'
),
path(
    'buyer/orders/<int:order_id>/',
    views.buyer_order_detail,
    name='buyer_order_detail'
),
path(
    'product/<int:product_id>/',
    views.product_detail,
    name='product_detail'
),

]

