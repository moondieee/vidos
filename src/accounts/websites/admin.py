from django.contrib import admin

from .models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'url', 'description')
    search_fields = ('name', 'user__username', 'url')
    list_filter = ('user',)

    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Информация о сайте', {
            'fields': ('name', 'url', 'description'),
        }),
    )
