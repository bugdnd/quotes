from django.contrib import admin
from .models import Source, Quote, Like


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type']
    list_filter = ['source_type']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'source', 'weight', 'views_count', 'created_at']
    list_filter = ['source', 'created_at']
    search_fields = ['text']
    
    def text_short(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['quote_short', 'is_like', 'ip_address', 'created_at']
    list_filter = ['is_like', 'created_at']
    
    def quote_short(self, obj):
        return obj.quote.text[:30] + "..." if len(obj.quote.text) > 30 else obj.quote.text
    quote_short.short_description = 'Цитата'