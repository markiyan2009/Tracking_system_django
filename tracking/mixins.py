from django.core.exceptions import PermissionDenied


class UserIsAssignedTaskMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.column.project.owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class UserIsAssignedCommentkMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    