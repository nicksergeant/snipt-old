from django.contrib.auth.models import User
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_superuser', 'date_joined')
    search_fields = ['username', 'email']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
