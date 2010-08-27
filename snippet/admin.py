from snipt.snippet.models import Snippet
from django.contrib import admin

class SnippetAdmin(admin.ModelAdmin):
    list_display = ('description','user','slug','created',)
    ordering = ('created',)
    prepopulated_fields = {'slug': ('description',)}
    
admin.site.register(Snippet, SnippetAdmin)
