from rest_framework import permissions

from .models import Time


class IsVoteTimePermission(permissions.BasePermission):
    message = 'Now is not vote time.'

    def has_permission(self, request, view):
        time = Time.objects.first()
        if time is None:
            return False

        return time.is_vote_time
