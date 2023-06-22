from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import (ProductsListView, ProductDeleteView, ProductCreateView, ProductDetailsView, ProductUpdateView,
                    RegisterView, MyLogoutView, AboutMeView, AboutMeUpdateView, Search, view_cart, add_to_cart,
                    remove_from_cart, create_order, ProductSortHView, ProductSortLView, )
from .views import shop_index

app_name = "shopapp"
urlpatterns = [
    path("", shop_index, name="index"),
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(template_name="shopapp/login.html", redirect_authenticated_user=True, ),
         name="login"),
    path("logout/", MyLogoutView.as_view(), name='logout'),
    path("about-me/", AboutMeView.as_view(), name='about-me'),
    path("about-me/<int:pk>/update/", AboutMeUpdateView.as_view(), name="profile-update"),
    path("products/", ProductsListView.as_view(), name="products-list"),
    path("productsh/", ProductSortHView.as_view(), name="product-sorth"),
    path("productsl/", ProductSortLView.as_view(), name="product-sortl"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("products/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/create", ProductCreateView.as_view(), name="product-create"),
    path("search", Search.as_view(), name="search"),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', create_order, name='create_order'),
]
