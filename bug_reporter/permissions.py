from rest_framework import permissions
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)


class IsTeamMember(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.data)
        if request.method == 'GET':
            return True
        project = view.queryset[0]
        users = project.users.all()
        print(users)
        return True
        # project = request.project
        # user = request.user
        # if user.IsMaster or user in list(project.users):
        #     return True
        # return False