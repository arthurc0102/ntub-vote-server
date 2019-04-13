from django.contrib import admin

from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('std_no', 'name', 'klass', 'pool')
    list_filter = ('pool',)
    add_fieldsets = (
        (None, {
            'fields': ('image', 'std_no', 'politics', 'pool'),
        }),
    )
    readonly_fields = ('name', 'klass')

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        return super().get_fieldsets(request, obj)
