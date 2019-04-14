from django import forms
from django.core.exceptions import ValidationError

from app.school.services import get_student_info

from .models import Vote


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'

    def clean(self):
        errors = {}
        cleaned_data = super().clean()
        std_no = cleaned_data.get('std_no')
        candidate = cleaned_data.get('candidate')

        if not std_no or not candidate:
            return

        try:
            info = get_student_info(std_no, ['dept_print'])
        except Exception:
            errors.setdefault('std_no', []).append(
                'Student number not valid.',
            )
        else:
            departments = candidate \
                .pool.departments \
                .values_list('name', flat=True)

            if info['dept_print'] not in departments:
                errors.setdefault('candidate', []).append(
                    'You can\'t vote to this candidate.',
                )

        if errors:
            raise ValidationError(errors)
