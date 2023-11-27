from rest_framework import permissions

from .exceptions import UnauthorizedException

def check_user_information(user):
    if not user.is_authenticated:
        raise UnauthorizedException('Authentication credentials were not provided.')

    if not hasattr(user, 'information'):
        raise UnauthorizedException('User has not finished registration.')
    return

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        check_user_information(request.user)
        return request.user.information.is_admin

class IsCanteenOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        check_user_information(request.user)
        return request.user.information.role == 'Pemilik Kantin'
    
class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        check_user_information(request.user)
        return request.user.information.role == 'User'