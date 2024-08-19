from django.contrib import admin
from .models import Tests, Results


@admin.register(Tests)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'for_who', 'time_limit', 'created_at', 'red_line')
    search_fields = ('title', 'for_who')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(Results)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'test', 'user', 'counts_true', 'counts_false', 'time_duration', 'is_successful',
        'created_at')
    search_fields = ('user__full_name', 'test__title')
    date_hierarchy = 'created_at'
    list_filter = ('created_at', 'is_successful', 'time_duration')
    readonly_fields = (
        'id', 'test', 'user', 'counts_true', 'counts_false', 'time_duration', 'is_successful', 'created_at')
