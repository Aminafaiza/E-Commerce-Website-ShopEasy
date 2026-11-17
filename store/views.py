from django.views.decorators.http import require_POST
from decimal import Decimal
from functools import wraps
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .decorators import buyer_required
from .models import Category, Product ,Order, OrderItem
from .forms import RegisterForm, ProductForm
from .decorators import seller_required
from django.views.decorators.cache import never_cache
# ==========================================
# BUYER-ONLY ACCESS
# ==========================================

def buyer_required(view_func):

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.role != 'buyer':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


# ==========================================
# SELLER-ONLY ACCESS
# ==========================================

def seller_required(view_func):

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.role != 'seller':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


# ==========================================
# USER REGISTRATION
# ==========================================

def register_view(request):

    if request.user.is_authenticated:

        if request.user.role == 'seller':
            return redirect('seller_dashboard')

        return redirect('buyer_dashboard')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Registration successful! Please login.'
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'store/register.html',
        {'form': form}
    )


# ==========================================
# USER LOGIN
# ==========================================

def login_view(request):

    if request.user.is_authenticated:

        if request.user.role == 'seller':
            return redirect('seller_dashboard')

        return redirect('buyer_dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == 'seller':
                return redirect('seller_dashboard')

            return redirect('buyer_dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'store/login.html'
    )


# ==========================================
# USER LOGOUT
# ==========================================

@login_required
def logout_view(request):

    if request.method == 'POST':

        logout(request)

        messages.success(
            request,
            'You have logged out successfully.'
        )

        return redirect('login')

    if request.user.role == 'seller':
        return redirect('seller_dashboard')

    return redirect('buyer_dashboard')

@login_required(login_url='login')
@never_cache
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(
            request,
            'You have logged out successfully.'
        )
        return redirect('login')

    return redirect('home')

# ==========================================
# BUYER DASHBOARD
# ==========================================

@buyer_required
def buyer_dashboard(request):

    return render(
        request,
        'store/buyer_dashboard.html'
    )


# ==========================================
# SELLER DASHBOARD
# ==========================================

@seller_required
def seller_dashboard(request):

    return render(
        request,
        'store/seller_dashboard.html'
    )


# ==========================================
# SHOPEASY HOMEPAGE
# ==========================================

def home_view(request):

    # Display all active products, including out-of-stock products
    products = Product.objects.filter(
        is_active=True
    ).select_related('category', 'seller')

    categories = Category.objects.all()

    search_query = request.GET.get('q', '').strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }

    return render(
        request,
        'store/home.html',
        context
    )


# ==========================================
# SELLER: VIEW MY PRODUCTS
# ==========================================

@seller_required
def seller_products(request):

    products = Product.objects.filter(
        seller=request.user
    ).select_related('category')

    return render(
        request,
        'store/seller_products.html',
        {'products': products}
    )


# ==========================================
# SELLER: ADD PRODUCT
# ==========================================

@seller_required
def add_product(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(commit=False)

            product.seller = request.user

            product.save()

            messages.success(
                request,
                'Product added successfully!'
            )

            return redirect('seller_products')

    else:
        form = ProductForm()

    return render(
        request,
        'store/add_product.html',
        {'form': form}
    )


# ==========================================
# SELLER: EDIT PRODUCT
# ==========================================

@seller_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product updated successfully!'
            )

            return redirect('seller_products')

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'store/edit_product.html',
        {
            'form': form,
            'product': product
        }
    )


# ==========================================
# SELLER: DELETE PRODUCT
# ==========================================

@seller_required
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == 'POST':

        product.delete()

        messages.success(
            request,
            'Product deleted successfully!'
        )

        return redirect('seller_products')

    return render(
        request,
        'store/delete_product.html',
        {'product': product}
    )


# ==========================================
# BUYER: ADD PRODUCT TO CART
# ==========================================

@buyer_required
@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    current_quantity = int(cart.get(product_id, 0))

    if current_quantity + 1 > product.stock:

        messages.error(
            request,
            f"Only {product.stock} units of {product.name} are available."
        )

    else:

        cart[product_id] = current_quantity + 1

        request.session['cart'] = cart

        messages.success(
            request,
            f"{product.name} added to your cart!"
        )

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ==========================================
# BUYER: VIEW SHOPPING CART
# ==========================================

@buyer_required
def cart_view(request):

    cart = request.session.get('cart', {})

    cart_items = []
    total = Decimal('0.00')

    for product_id, quantity in list(cart.items()):

        try:
            quantity = int(quantity)

            if quantity <= 0:
                raise ValueError

            product = Product.objects.get(
                id=product_id,
                is_active=True
            )

        except (
            Product.DoesNotExist,
            ValueError,
            TypeError
        ):

            cart.pop(product_id, None)
            continue

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    request.session['cart'] = cart

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# ==========================================
# BUYER: UPDATE CART QUANTITY
# ==========================================

@buyer_required
@require_POST
def update_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    try:
        quantity = int(request.POST.get('quantity', 1))

    except (ValueError, TypeError):

        messages.error(
            request,
            "Please enter a valid quantity."
        )

        return redirect('cart')

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if quantity < 1:

        messages.error(
            request,
            "Quantity must be at least 1."
        )

    elif quantity > product.stock:

        messages.error(
            request,
            f"Only {product.stock} units of {product.name} are available."
        )

    else:

        cart[product_id] = quantity

        request.session['cart'] = cart

        messages.success(
            request,
            "Cart quantity updated successfully!"
        )

    return redirect('cart')


# ==========================================
# BUYER: REMOVE PRODUCT FROM CART
# ==========================================

@buyer_required
@require_POST
def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

        request.session['cart'] = cart

        messages.success(
            request,
            "Product removed from your cart."
        )

    return redirect('cart')

# ==========================================
# BUYER: MY ORDERS
# ==========================================
@buyer_required
def buyer_orders(request):

    orders = Order.objects.filter(
        buyer=request.user
    ).prefetch_related(
        'items',
        'items__product'
    ).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(
        request,
        'store/buyer_orders.html',
        context
    )
@buyer_required
def buyer_order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            'items',
            'items__product'
        ),
        id=order_id,
        buyer=request.user
    )

    return render(
        request,
        'store/buyer_order_detail.html',
        {'order': order}
    )
@buyer_required
def checkout_view(request):

    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    cart_items = []
    total = Decimal('0.00')

    # Prepare checkout items
    for product_id, quantity in cart.items():

        try:
            quantity = int(quantity)

            if quantity <= 0:
                continue

            product = Product.objects.get(
                id=product_id,
                is_active=True
            )

            if quantity > product.stock:
                messages.error(
                    request,
                    f"Only {product.stock} units of {product.name} are available."
                )
                return redirect('cart')

            subtotal = product.price * quantity

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

            total += subtotal

        except (Product.DoesNotExist, ValueError, TypeError):
            messages.error(
                request,
                "One of the products in your cart is no longer available."
            )
            return redirect('cart')

    if not cart_items:
        request.session['cart'] = {}
        messages.warning(request, "Your cart has no valid products.")
        return redirect('cart')

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'store/checkout.html', context)

@buyer_required
@require_POST
def place_order(request):

    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    # Read delivery details
    full_name = request.POST.get('full_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    postal_code = request.POST.get('postal_code', '').strip()

    # Basic validation
    if not all([
        full_name,
        phone,
        address,
        city,
        state,
        postal_code
    ]):
        messages.error(request, "Please complete all delivery details.")
        return redirect('checkout')

    if len(phone) > 15 or len(postal_code) > 10:
        messages.error(request, "Please check your phone number and postal code.")
        return redirect('checkout')

    try:
        with transaction.atomic():

            order_items_data = []
            total = Decimal('0.00')

            # Recheck stock immediately before creating the order
            for product_id, quantity in cart.items():

                quantity = int(quantity)

                if quantity <= 0:
                    raise ValueError("Invalid product quantity.")

                product = Product.objects.select_for_update().get(
                    id=product_id,
                    is_active=True
                )

                if product.stock < quantity:
                    raise ValueError(
                        f"Not enough stock for {product.name}. "
                        f"Available quantity: {product.stock}."
                    )

                subtotal = product.price * quantity
                total += subtotal

                order_items_data.append({
                    'product': product,
                    'product_name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'subtotal': subtotal,
                })

            if not order_items_data:
                raise ValueError("Your cart does not contain valid products.")

            # Create the main order
            order = Order.objects.create(
                buyer=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                payment_method='cod',
                total_amount=total,
            )

            # Create order items and reduce stock
            for item in order_items_data:

                OrderItem.objects.create(
                    order=order,
                    **item
                )

                product = item['product']
                product.stock -= item['quantity']
                product.save(update_fields=['stock'])

        # Clear the cart only after the transaction succeeds
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    except (Product.DoesNotExist, ValueError, TypeError) as error:
        messages.error(request, str(error))
        return redirect('cart')

@buyer_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    return render(
        request,
        'store/order_success.html',
        {'order': order}
    )
@seller_required
def seller_orders(request):

    orders = OrderItem.objects.filter(
        product__seller=request.user
    ).select_related(
        'order',
        'order__buyer',
        'product'
    ).order_by('-order__created_at')

    context = {
        'orders': orders,
    }

    return render(
        request,
        'store/seller_orders.html',
        context
    )

@seller_required
@require_POST
def update_order_status(request, item_id):

    order_item = get_object_or_404(
        OrderItem,
        id=item_id,
        product__seller=request.user
    )

    new_status = request.POST.get('status')

    valid_statuses = dict(OrderItem.STATUS_CHOICES)

    if new_status not in valid_statuses:
        messages.error(request, "Invalid order status.")
        return redirect('seller_orders')

    order_item.status = new_status
    order_item.save(update_fields=['status'])

    messages.success(
        request,
        f"Order #{order_item.order.id} status updated to "
        f"{valid_statuses[new_status]}."
    )

    return redirect('seller_orders')

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    return render(
        request,
        'store/product_detail.html',
        {'product': product}
    )