from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.members_list, name='members_list'),

    # Product
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Favorites
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/toggle/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Static pages
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
