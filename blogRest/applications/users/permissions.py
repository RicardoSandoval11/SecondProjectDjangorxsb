from rest_framework import permissions

class IsAdministraror(permissions.BasePermission):

    message = 'You do not have the permissions to access to this resources'

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user.ocupation == 'A'
        else:
            return False
        


class IsWorker(permissions.BasePermission):

    message = 'You do not have the permissions to access to this resources'

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user.ocupation == 'W'
        else:
            return False

class IsUser(permissions.BasePermission):

    message = 'You do not have the permissions to access to this resources'

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user.ocupation == 'U'
        else:
            return False