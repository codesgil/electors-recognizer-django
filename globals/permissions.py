from rest_framework import permissions
from users.models import User, BlackListedToken
from users import constants
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import NotFound, PermissionDenied


def _has_role_permission(role, roles):
    if role in roles:
        return True
    return False


def resource_not_found(view):
    if not view.action:
        raise NotFound(detail='Resource not found.')


def unauthorized():
    raise PermissionDenied()


def is_valid_token(request, types=constants.TOKEN):
    if request.user:
        user_id = request.user.id
        token = request.auth.token.decode("utf-8")
        blacklisted_token = BlackListedToken.objects.filter(user=user_id, token=token, type=types)
        if blacklisted_token:
            raise InvalidToken()


class HasCredential(permissions.BasePermission):
    def has_permission(self, request, view):
        resource_not_found(view)
        user = request.user
        if isinstance(user, User):
            is_valid_token(request)
            return True
        raise InvalidToken()


class IsAdminUser(permissions.BasePermission):
    list_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    create_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    update_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    delete_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    me_password_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR,
                         constants.ROLE_USER]

    def has_permission(self, request, view):
        resource_not_found(view)
        user = request.user
        if isinstance(user, User):
            is_valid_token(request)
            if view.action == 'list':
                return _has_role_permission(user.role, self.list_roles)
            elif view.action == 'create' or view.action == 'check_username':
                return _has_role_permission(user.role, self.create_roles)
            elif view.action == 'update':
                return _has_role_permission(user.role, self.update_roles)
            elif view.action == 'destroy':
                return _has_role_permission(user.role, self.delete_roles)
            elif view.action == 'me' or view.action == 'change_password':
                return _has_role_permission(user.role, self.me_password_roles)
            elif view.action == 'retrieve':
                return _has_role_permission(user.role, self.list_roles)
        return False


class IsTeamUser(permissions.BasePermission):
    list_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR, constants.ROLE_USER]
    create_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    update_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    delete_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]
    export_roles = [constants.ROLE_SUPER_ADMIN, constants.ROLE_ADMIN, constants.ROLE_SUPERVISOR]

    def has_permission(self, request, view):
        resource_not_found(view)
        user = request.user
        if isinstance(user, User):
            is_valid_token(request)
            if view.action == 'list' or view.action == 'statistic':
                return _has_role_permission(user.role, self.list_roles)
            elif view.action == 'create':
                return _has_role_permission(user.role, self.create_roles)
            elif view.action == 'update':
                return _has_role_permission(user.role, self.update_roles)
            elif view.action == 'destroy':
                return _has_role_permission(user.role, self.delete_roles)
            elif view.action == 'retrieve':
                return _has_role_permission(user.role, self.list_roles)
            elif view.action == 'export':
                return _has_role_permission(user.role, self.export_roles)
        return False
