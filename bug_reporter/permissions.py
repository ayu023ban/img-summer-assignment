from rest_framework import permissions
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)


class CustomAuthentication(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.isDisabled:
            return False

class IsTeamMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        users = project.users.all()
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.isMaster or request.user in list(users):
            return True
        return False


class IsCreatorOfProject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method =='DELETE':
            return request.user == obj.creator
        return super().has_object_permission(request, view, obj)


class IsOwnerOfUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user == obj or request.user.isMaster

class IsMaster(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.isMaster