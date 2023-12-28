from rest_framework.permissions import BasePermission


class IsActiveOrStaff(BasePermission):
    """ Дает доступ к Апи только активным сотрудникам или модераторам """

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser or request.user.is_active:
            return True
