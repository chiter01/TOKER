from django.contrib import admin
from .models import Furniture, Category, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') 
    search_fields = ('name',) 


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1 
    fields = ('user', 'stars', 'comment', 'created_at')
    readonly_fields = ('created_at',) 


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'popularity', 'rating')  
    list_filter = ('available', 'category')  
    search_fields = ('name', 'description')  
    readonly_fields = ('popularity', 'rating')  
    inlines = [ReviewInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'category', 'image', 'available')
        }),
        ('Статистика', {
            'fields': ('popularity', 'rating'),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('furniture', 'user', 'stars', 'comment', 'created_at')  
    list_filter = ('stars', 'created_at')  
    search_fields = ('furniture__name', 'user__username', 'comment') 
