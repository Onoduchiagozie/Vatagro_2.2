from django.urls import path
from . import views

urlpatterns = [
    # ── Core pages ────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.SignUpView.as_view(), name='register'),

    # ── Products & categories ─────────────────────────────────────
    path('category/<pk>', views.category, name='category'),

    # FIX #5: was path('category/<pk>') — identical to the line above,
    # making category2 completely unreachable. Changed to by_location/<pk>.
    # Update any {% url 'category2' pk %} tags in your templates to match.
    path('by_location/<pk>', views.category2, name='category2'),

    path('product_details/<pk>', views.product_details, name='product_details'),
    path('product_details2', views.search_product_details, name='product_details2'),
    path('submit_review/<int:product_id>', views.review_rating, name='submit_review'),

    # ── Cart & checkout ───────────────────────────────────────────
    path('checkout', views.checkout, name='checkout'),
    path('addcart/<int:product_id>', views.add_cart, name='addcart'),
    path('addcart2/<int:product_id>', views.add_cart2, name='addcart2'),
    path('removecart/<int:product_id>', views.remove_cart, name='removecart'),
    path('clearcart', views.clear_cart, name='clearcart'),

    # ── Stripe payment ────────────────────────────────────────────
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]