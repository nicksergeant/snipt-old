from snipt.ad.models import Ad
from django.contrib import admin

class AdAdmin(admin.ModelAdmin):
    list_display = ('title','tags','url','image',)
    ordering = ('title',)
    
admin.site.register(Ad, AdAdmin)
