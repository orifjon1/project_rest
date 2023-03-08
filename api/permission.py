from rest_framework.permissions import BasePermission


class IsDirectorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and (request.user.status == 'director' or request.user.status == 'manager'):
            return True
        elif request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return False


class IsWorkerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' and (request.user.status == 'employee' or request.user.status == 'manager'):
            return True
        return False


class CanWriteReview(BasePermission):
    """
    Custom permission to allow only assigned user or assigner user to write review.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user making the request is either the assigned user or the assigner user for the Task model.
        """
        return obj.boss == request.user or obj.worker == request.user
