from snipt.favsnipt.models import FavSnipt
from django.contrib import admin

class FavSniptAdmin(admin.ModelAdmin):
    list_display = ('snipt','user','created',)
    ordering = ('created',)
    
admin.site.register(FavSnipt, FavSniptAdmin)
