from django.contrib import admin

from .models import Department


@admin.register(Department)
class DisplayNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
