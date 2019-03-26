from django.contrib import admin

from .models import System, Department, Grade, Class


admin.site.register(System)
admin.site.register(Department)
admin.site.register(Grade)
admin.site.register(Class)
