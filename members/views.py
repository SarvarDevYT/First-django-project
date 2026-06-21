from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product, Category, CartItem, Favorite, UserProfile, Order, OrderItem


# ─── Helper: context processor for sidebar counts ───────────────────────────
def _base_context(request):
    ctx = {}
    if request.user.is_authenticated:
        ctx['cart_count'] = CartItem.objects.filter(user=request.user).count()
        ctx['favorites_count'] = Favorite.objects.filter(user=request.user).count()
        ctx['favorite_ids'] = list(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    else:
        ctx['cart_count'] = 0
        ctx['favorites_count'] = 0
        ctx['favorite_ids'] = []
    ctx['categories'] = Category.objects.prefetch_related('products').all()
    return ctx


# ─── Home Page ───────────────────────────────────────────────────────────────
def members_list(request):
    q = request.GET.get('q', '').strip()
    cat_slug = request.GET.get('cat', '').strip()

    products = Product.objects.select_related('category').all()
    if q:
        products = products.filter(title__icontains=q)
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    # Trending Items = barcha mahsulotlar (yangilari birinchi), max 20
    trending_products = Product.objects.select_related('category').order_by('-created_at')[:20]

    ctx = _base_context(request)
    ctx.update({
        'products': products,
        'trending_products': trending_products,
        'active_category': cat_slug,
        'search_query': q,
    })
    return render(request, 'members/index.html', ctx)


# ─── Product Detail ──────────────────────────────────────────────────────────
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ctx = _base_context(request)
    ctx['product'] = product
    return render(request, 'members/product_detail.html', ctx)


# ─── Cart ────────────────────────────────────────────────────────────────────
@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    ctx = _base_context(request)
    ctx.update({'cart_items': cart_items, 'total': total})
    return render(request, 'members/cart.html', ctx)


@login_required(login_url='login')
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        item, created = CartItem.objects.get_or_create(
            user=request.user, product=product,
            defaults={'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()
        messages.success(request, f'"{product.title}" savatga qo\'shildi.')
    return redirect(request.META.get('HTTP_REFERER', 'members_list'))


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, pk=item_id, user=request.user)
        item.delete()
        messages.success(request, 'Savatdan o\'chirildi.')
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            messages.warning(request, 'Savat bo\'sh.')
            return redirect('cart')

        total = sum(item.product.price * item.quantity for item in cart_items)
        address = request.POST.get('address', '').strip()
        note = request.POST.get('note', '').strip()

        # Buyurtma yaratish
        order = Order.objects.create(
            user=request.user,
            total=total,
            address=address,
            note=note,
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                title=item.product.title,
                price=item.product.price,
                quantity=item.quantity,
            )

        # Savatni tozalash
        cart_items.delete()
        messages.success(request, f'Buyurtma #{order.pk} muvaffaqiyatli qabul qilindi!')
        return redirect('order_success', pk=order.pk)

    return redirect('cart')


@login_required(login_url='login')
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    ctx = _base_context(request)
    ctx['order'] = order
    return render(request, 'members/order_success.html', ctx)


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    ctx = _base_context(request)
    ctx['orders'] = orders
    return render(request, 'members/my_orders.html', ctx)


# ─── Favorites ───────────────────────────────────────────────────────────────
@login_required(login_url='login')
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    ctx = _base_context(request)
    ctx['favorites'] = favorites
    return render(request, 'members/favorites.html', ctx)


@login_required(login_url='login')
def toggle_favorite(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            fav.delete()
            messages.info(request, f'"{product.title}" sevimlidan olib tashlandi.')
        else:
            messages.success(request, f'"{product.title}" sevimlilarga qo\'shildi.')
    return redirect(request.META.get('HTTP_REFERER', 'members_list'))


# ─── Profile ─────────────────────────────────────────────────────────────────
@login_required(login_url='login')
def profile_view(request):
    recommended = Product.objects.order_by('?')[:6]
    ctx = _base_context(request)
    ctx['recommended'] = recommended
    return render(request, 'members/profile.html', ctx)


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)

        phone_raw = request.POST.get('phone', '').strip()
        if phone_raw:
            new_phone = '+998' + phone_raw if not phone_raw.startswith('+') else phone_raw
            # Check if this phone belongs to a DIFFERENT user
            conflict = UserProfile.objects.filter(phone=new_phone).exclude(user=user).first()
            if conflict:
                messages.error(request, 'Bu telefon raqam allaqachon boshqa foydalanuvchiga tegishli.')
                ctx = _base_context(request)
                return render(request, 'members/edit_profile.html', ctx)
            profile.phone = new_phone

        profile.gender = request.POST.get('gender', '')
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()

        messages.success(request, 'Profil muvaffaqiyatli yangilandi.')
        return redirect('profile')

    ctx = _base_context(request)
    return render(request, 'members/edit_profile.html', ctx)


# ─── Auth ────────────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('members_list')

    if request.method == 'POST':
        phone_raw = request.POST.get('phone', '').strip()
        phone = '+998' + phone_raw if phone_raw and not phone_raw.startswith('+') else phone_raw

        # Find or create user by phone
        try:
            profile = UserProfile.objects.get(phone=phone)
            user = profile.user
        except UserProfile.DoesNotExist:
            # Create new user
            username = 'user_' + phone_raw.replace(' ', '')
            user, created = User.objects.get_or_create(username=username)
            profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'phone': phone})
            if not created:
                profile.phone = phone
                profile.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        messages.success(request, 'Xush kelibsiz!')
        return redirect('members_list')

    ctx = _base_context(request)
    return render(request, 'members/login.html', ctx)


def logout_view(request):
    logout(request)
    messages.info(request, 'Tizimdan chiqildi.')
    return redirect('members_list')


# ─── Static Pages ────────────────────────────────────────────────────────────
def about_view(request):
    ctx = _base_context(request)
    return render(request, 'members/about.html', ctx)


def contact_view(request):
    ctx = _base_context(request)
    return render(request, 'members/contact.html', ctx)