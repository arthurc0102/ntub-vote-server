from django.contrib import admin

from .models import Time, Pool, Vote


admin.site.register(Time)
admin.site.register(Pool)
admin.site.register(Vote)
