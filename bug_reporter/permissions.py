from rest_framework import permissions

class CustomAuthentication(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.isDisabled


class IsTeamMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj
        users = project.users.all()
        return request.user and request.user in list(users) or request.user.isMaster
           
class IsCreatorOfObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.isMaster

class IsMaster(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.isMaster

class IsMemberOfProjectOfCurrentIssue(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        issue = obj
        project = issue.project
        users = project.users.all()
        return request.user and request.user in list(users) or request.user.isMaster