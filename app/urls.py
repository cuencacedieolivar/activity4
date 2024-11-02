from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (CustomLoginView ,RegisterView, CustomLogoutView,
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, CategoryListView, CategoryDetailView,
    OrderListView, OrderDetailView, HomePageView, CartView, AddToCartView,RemoveCartItemView,
    UpdateCartItemView, CheckoutView, OrderSuccessView, ReviewListView, ReviewCreateView,AdminProductListView,category_search
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # Home Page
    path('', HomePageView.as_view(), name='home'),

    # Product URLs

    path('admin_product_list', AdminProductListView.as_view(), name='admin_product_list'),  # Ensure this matches
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),


    # Review URLs
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review_list'),
    path('products/<int:product_id>/reviews/new/', ReviewCreateView.as_view(), name='review_create'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/search/', category_search, name='category_search'),  # Add the category search URL

    # Order URLs
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

    # Cart URLs
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),

    # Checkout and Order Success
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),  # Separate view for order success
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
