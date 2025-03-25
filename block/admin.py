from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','verification_code','is_verified',)
    readonly_fields = ('verification_code','is_verified',)

# Register your models here.
