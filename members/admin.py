from django.contrib import admin
from .models import Category, Product, UserProfile, CartItem, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Mahsulotlar soni"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ('title', 'category', 'vendor', 'price', 'old_price', 'is_trending', 'created_at')
    list_filter    = ('category', 'is_trending', 'vendor')
    search_fields  = ('title', 'vendor')
    list_editable  = ('is_trending',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'title', 'vendor', 'image', 'is_trending')
        }),
        ('Narx', {
            'fields': ('price', 'old_price')
        }),
        ('Texnik xususiyatlar', {
            'fields': ('display_size', 'processor', 'internal_memory',
                       'camera', 'battery_info', 'color'),
            'classes': ('collapse',),
        }),
        ('Meta', {
            'fields': ('created_at',),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender')
    search_fields = ('user__username', 'phone')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter  = ('user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter  = ('user',)
