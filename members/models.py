from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Slug (URL uchun)")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name="Kategoriyasi")
    title = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    vendor = models.CharField(max_length=100, blank=True, null=True, verbose_name="Brend (Masalan: APPLE, NIKE)")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi (so'mda)")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True,
                                    verbose_name="Eski narxi (Chegirma uchun)")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Asosiy rasm")

    display_size = models.CharField(max_length=100, blank=True, null=True, verbose_name="Displey hajmi")
    processor = models.CharField(max_length=150, blank=True, null=True, verbose_name="Protsessor modeli")
    internal_memory = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ichki xotira")
    camera = models.CharField(max_length=150, blank=True, null=True, verbose_name="Kamera o'lchamlari")
    battery_info = models.CharField(max_length=150, blank=True, null=True, verbose_name="Batareya xususiyati")
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name="Rangi")

    is_trending = models.BooleanField(default=False, verbose_name="Trending Items qismiga chiqarish")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefon raqami")
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name="Profil rasmi")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Jinsi")

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} profili"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Foydalanuvchi")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Savatga qo'shilgan vaqt")

    class Meta:
        verbose_name = "Savatdagi maxsulot"
        verbose_name_plural = "Savatdagi maxsulotlar"

    def __str__(self):
        return f"{self.user.username} savatida: {self.product.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Foydalanuvchi")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sevimlilarga qo'shilgan mahsulot")

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Sevimli maxsulot"
        verbose_name_plural = "Sevimlilar ro'yxati"

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('delivered',  'Yetkazildi'),
        ('cancelled',  'Bekor qilindi'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Foydalanuvchi")
    total      = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Jami summa")
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    address    = models.TextField(blank=True, null=True, verbose_name="Yetkazish manzili")
    note       = models.TextField(blank=True, null=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma vaqti")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.pk} — {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Buyurtma")
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Mahsulot")
    title    = models.CharField(max_length=255, verbose_name="Mahsulot nomi (snapshot)")
    price    = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")

    class Meta:
        verbose_name = "Buyurtma qatori"
        verbose_name_plural = "Buyurtma qatorlari"

    def __str__(self):
        return f"{self.title} x{self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
