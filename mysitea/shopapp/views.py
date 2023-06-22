from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DeleteView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from .models import Profile
from django.db.models import Q


from .models import Product, CartItem, Order, OrderItem, Parameter, Cart

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.all()

def shop_index(request: HttpRequest) -> HttpResponse:
    products = Product.objects.order_by('-id')[:3]
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'shopapp/shop-index.html', context={'num_visits': num_visits, 'products': products})

class ProductSortHView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.all().order_by('-price')

class ProductSortLView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.all().order_by('price')

class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = "product"

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "shopapp.change_product"
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )



class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shopapp.delete_product"

    model = Product
    template_name = 'shopapp/products-delete.html'

    def get_success_url(self):
        return reverse(
            "shopapp:products-list",
        )



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "shopapp/register.html"
    success_url = reverse_lazy("shopapp:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class AboutMeView(TemplateView):
    template_name = "shopapp/about-me.html"

class AboutMeUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return True
    model = Profile
    fields = "user", 'last_name', 'first_name', 'email',
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:about-me",
        )

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("shopapp:login")


class Search(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(name__iregex=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'shopapp/cart.html', context)

def add_to_cart(request, pk):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(pk=pk)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shopapp:view_cart')


def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    return redirect('shopapp:view_cart')

def create_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    order = Order(user=request.user, total=0)
    order.save()
    for item in cart_items:
        order_item = OrderItem(order=order, product=item.product, quantity=item.quantity)
        order_item.save()
        order.total += item.product.price * item.quantity
    order.save()
    cart_items.delete()
    return redirect('shopapp:view_cart')
def product_catalog(request):
    products = Product.objects.all()
    parameters = Parameter.objects.all()
    if request.GET:
        query = Q()
        for key, value in request.GET.items():
            if value:
                query &= Q(productparameter__parameter__name=key, productparameter__value=value)
        products = products.filter(query)

    for product in products:
        ProductView.objects.create(product=product)

    context = {
        'products': products,
        'parameters': parameters,
    }
    return render(request, 'main/catalog.html', context)