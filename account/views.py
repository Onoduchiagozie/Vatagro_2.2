import random
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from account.forms import ReviewForm, SignUpForm
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from account.models import User
from farmer.models import Cart, CartItem
from goods.models import Category, StoreLocation
from goods.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from orders.models import OrderProducts, ReviewRating
import stripe
from django.core.mail import send_mail


# ─────────────────────────────────────────────
#  CART HELPERS
# ─────────────────────────────────────────────

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    # FIX: use get_object_or_404 instead of bare .get() to give a clean 404
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=cart)

    return redirect('checkout')


def add_cart2(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=cart)

    return redirect('product_details', pk=product_id)


def remove_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('checkout')


def clear_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        CartItem.objects.filter(cart=cart).delete()
    except Cart.DoesNotExist:
        pass
    return redirect('checkout')


# ─────────────────────────────────────────────
#  ORDER SUCCESS / CANCEL
# ─────────────────────────────────────────────

def success(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)

        for x in cart_items:
            # FIX #6: sold_by is now a ForeignKey — pass the User object directly
            # (previously passed x.product.farmername which saved a string repr)
            OrderProducts.objects.create(
                user=request.user,
                product_name=x.product.product_name,
                location=x.product.store_location.states if x.product.store_location else '',
                tracking_no='Vatagro-' + str(random.randint(10000, 99999)),
                quantity=x.quantity,
                amount=x.product.price * x.quantity,
                sold_by=x.product.farmername,   # now a real FK assignment
            )

        cart_items.delete()
    except Cart.DoesNotExist:
        pass  # Cart already cleared or session expired — safe to show success

    return render(request, 'account/success.html')


def cancel(request):
    return render(request, 'account/cancel.html')


# ─────────────────────────────────────────────
#  STRIPE
# ─────────────────────────────────────────────

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        return JsonResponse({'publicKey': settings.STRIPE_PUBLISHABLE_KEY}, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items.exists():
                return JsonResponse({'error': 'Your cart is empty.'})

            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(
                    reverse('success')
                ) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('cancel')),
                payment_method_types=['card'],
                customer_email=request.user.email,
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'ngn',
                            'product_data': {'name': x.product.product_name},
                            'unit_amount': x.product.price * 100,
                        },
                        'quantity': x.quantity,
                    }
                    for x in cart_items
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'No cart found.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# ─────────────────────────────────────────────
#  CHECKOUT PAGE
# ─────────────────────────────────────────────

@login_required
def checkout(request, total=0, quantity=0, cart_items=None):
    # FIX: handle missing cart gracefully instead of crashing
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        cart_items = []

    current_user = get_object_or_404(User, pk=request.user.id)

    # FIX #4: check address exists before touching it — new users have None
    has_shipping = current_user.Active_Shipping_Address is not None

    shipping_total = 0
    tax = 0
    grand_total = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    if has_shipping:
        for cart_item in cart_items:
            user_state = current_user.Active_Shipping_Address.state
            product_state = (
                cart_item.product.store_location.states
                if cart_item.product.store_location else None
            )
            if user_state and product_state and user_state == product_state:
                # FIX: shipping fee fields are CharFields — cast safely with fallback
                fee = int(cart_item.product.intra_state_shipping_fee or 0)
            else:
                fee = int(cart_item.product.inter_state_shipping_fee or 0)
            shipping_total += fee

    tax = round((2 * total) / 100, 2)
    grand_total = total + tax + shipping_total

    context = {
        'quantity': quantity,
        'cart_items': cart_items,
        'address': current_user,
        'tax': tax,
        'total': total,
        'grand_total': grand_total,
        'shipping_total': shipping_total,
        'has_shipping': has_shipping,
    }
    return render(request, 'account/checkout.html', context)


# ─────────────────────────────────────────────
#  CATEGORIES / PRODUCTS
# ─────────────────────────────────────────────

def category(request, pk):
    cat = Category.objects.all()
    main_page_category_header = get_object_or_404(Category, pk=pk)
    product_category = Product.objects.filter(product_catgeory=pk)
    storelocat = StoreLocation.objects.all()
    context = {
        'cat': cat,
        'main': main_page_category_header,
        'prod_cat': product_category,
        'store_state_list': storelocat,
        'prod_found': product_category.count(),
    }
    return render(request, 'account/catgeory.html', context)


# FIX #5: category2 now uses a distinct URL path (by_location/<pk>)
# so it's no longer shadowed by category — see urls.py
def category2(request, pk):
    cat = Category.objects.all()
    storelocations = StoreLocation.objects.all()
    main_page_state_header = get_object_or_404(StoreLocation, pk=pk)
    product_category = Product.objects.filter(store_location=pk)
    context = {
        'cat': cat,
        'prod_cat': product_category,
        'store_state_list': storelocations,
        'prod_found': product_category.count(),
        'state_name': main_page_state_header,
    }
    return render(request, 'account/catgeory.html', context)


@login_required
def product_details(request, pk):
    selected_product = get_object_or_404(Product, pk=pk)
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), product=selected_product)
    review = ReviewRating.objects.filter(
        product_id=selected_product.id, status=True)
    context = {
        'product': selected_product,
        'incart': in_cart,
        'review': review,
    }
    return render(request, 'account/product_details.html', context)


@login_required
def search_product_details(request):
    prod_id = request.POST.get('prod')
    selected_product = get_object_or_404(Product, pk=prod_id)
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), product=selected_product)
    review = ReviewRating.objects.filter(
        product_id=selected_product.id, status=True)
    context = {
        'product': selected_product,
        'incart': in_cart,
        'review': review,
    }
    return render(request, 'account/product_details.html', context)


def review_rating(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your review has been updated.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                # FIX: was using assignment operator on messages.success (a bug —
                # messages.success = (...) overwrites the function itself)
                ReviewRating.objects.create(
                    subject=form.cleaned_data['subject'],
                    rating=form.cleaned_data['rating'],
                    review=form.cleaned_data['review'],
                    product_id=product_id,
                    user_id=request.user.id,
                )
                messages.success(request, 'Thank you, your review has been submitted.')
                return redirect(url)

    return redirect(url or 'home')


# ─────────────────────────────────────────────
#  HOMEPAGE
# ─────────────────────────────────────────────

def home(request):
    context = {
        'cat': Category.objects.all(),
        'seller': User.objects.filter(staff=True),
        'product_list': Product.objects.filter(is_active=True),
    }
    return render(request, 'account/index.html', context)


# ─────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────

def logout_request(request):
    logout(request)
    return redirect('home')


class MyLogin(SuccessMessageMixin, LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('account')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'