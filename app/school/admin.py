from django.contrib import admin

from .models import System, Department, Grade, Class


@admin.register(System, Department, Grade, Class)
class DisplayNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
