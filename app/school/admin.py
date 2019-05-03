from django.contrib import admin

from .models import Department, Group, Student


@admin.register(Department, Group)
class DisplayNameAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('std_no',)
