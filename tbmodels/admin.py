from django.contrib import admin
from .models import Users, Category, Posts


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'username', 'telegram_id')
    search_fields = ('full_name', 'phone', 'username', 'telegram_id')


class PostsInlineAdmin(admin.StackedInline):
    model = Posts
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostsInlineAdmin,)
    list_display = ('id', 'name', 'for_who')
    list_filter = ('for_who',)
    search_fields = ('name',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'created_time')
    search_fields = ('category__name',)
    readonly_fields = ('created_time',)
    date_hierarchy = 'created_time'
