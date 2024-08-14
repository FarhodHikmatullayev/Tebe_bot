from django.contrib import admin
from .models import Users, Category, Posts


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    pass
