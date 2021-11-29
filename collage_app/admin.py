from django.contrib import admin
from .models import Serie, Token


# @admin.register(Serie)
# class AdminToken(admin.ModelAdmin):
#     list_display = ('collection_id', 'description', 'title')
#     list_filter = ('collection_id', 'date')


@admin.register(Token)
class AdminToken(admin.ModelAdmin):
    list_display = ('collection_id', 'description', 'title')
    list_filter = ('collection_id', 'date')
