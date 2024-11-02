from django.urls import reverse_lazy, reverse
from .models import Product, Cart, CartItem , Order , Review , Category
from django.views import View
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect, get_object_or_404 , render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.db.models import Q




import logging

logger = logging.getLogger(__name__)



class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm  # Use your custom form
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout

class HomePageView(TemplateView):
    template_name = 'app/home.html'  # Create this template to display products





class ProductListView(TemplateView):
    template_name = 'app/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tools_products'] = Product.objects.filter(category__name="tool")  # Filter products by 'tools' category
        context['plant_products'] = Product.objects.filter(category__name="plant")  # Filter products by 'plant' category
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()  # Accessing reviews using related_name
        return context

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # Only allow staff users

class AdminProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'app/admin_product_list.html'
    context_object_name = 'products'  # Name of the variable in the template

    def get_queryset(self):
        return Product.objects.all()  # Get all products for admin view

class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'description', 'stock', 'type', 'image']
    template_name = 'app/product_create.html'
    success_url = reverse_lazy('admin_product_list')

class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'price', 'description', 'stock', 'type', 'image']
    template_name = 'app/product_update.html'
    success_url = reverse_lazy('admin_product_list')

class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'app/product_delete.html'
    success_url = reverse_lazy('admin_product_list')


def category_search(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    products = Product.objects.all()

    if query:
        # Filter categories based on name or description
        categories = categories.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

        # Filter products based on various fields
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |  # search in category name
            Q(type__icontains=query)  # search in product type
        ).distinct()

    context = {
        'categories': categories,
        'products': products,
        'query': query
    }
    return render(request, 'app/category_search.html', context)

class CategoryListView(ListView):
    model = Category
    template_name = 'app/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'app/category_detail.html'
    context_object_name = 'category'

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'app/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Only show orders for the logged-in user
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'app/order_detail.html'
    context_object_name = 'order'


class CartView(LoginRequiredMixin, View):
    template_name = 'app/cart.html'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total = sum(item.total_price() for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total': total,
        }
        return render(request, self.template_name, context)

class CartCountMixin:
    def get_cart_count(self, user):
        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
            return cart.items.count()
        return 0


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Get the quantity from the POST data; it defaults to 1 if not provided
        quantity = request.POST.get('quantity')

        # Ensure quantity is a positive integer
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError("Quantity must be at least 1")
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity. It must be a positive integer.")
            return redirect('product_detail', pk=product_id)

        # Get or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Set the quantity appropriately
        cart_item.quantity = quantity  # Set to the validated quantity
        cart_item.save()  # Save the cart item to the database

        messages.success(request, f"{product.name} has been added to your cart.")
        return redirect('cart')  # Redirect to the cart view after adding

class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        quantity = request.POST.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()
        return redirect('cart')


class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        # Delete the cart item
        cart_item.delete()

        messages.success(request, "Item removed from your cart.")
        return redirect('cart')


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'app/checkout.html'

    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        total = sum(item.total_price() for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total': total,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        if not cart_items:
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        # Check stock availability and place order
        for item in cart_items:
            product = item.product
            if item.quantity > product.stock:
                messages.warning(request, f"Insufficient stock for {product.name}. Order not placed.")
                return redirect('cart')

        # If stock is available, reduce stock and create order
        for item in cart_items:
            product = item.product
            product.stock -= item.quantity
            product.save()
            Order.objects.create(user=request.user, product=product, quantity=item.quantity)

        # Clear cart after successful checkout
        cart.items.all().delete()
        messages.success(request, "Your order has been placed successfully!")  # Set success message
        return redirect('order_success')  # Redirect to a success page instead of login


class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'app/order_success.html'


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'app/add_review.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        form.instance.user = self.request.user
        form.instance.product = product
        messages.success(self.request, "Review added.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_detail', args=[self.kwargs['product_id']])


class ReviewListView(ListView):
    model = Review
    template_name = 'app/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'app/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product_id = self.kwargs['product_id']  # Get the product ID from URL
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.kwargs['product_id']})