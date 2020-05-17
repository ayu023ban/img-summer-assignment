from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r'projectsvi',ProjectViewSet)
router.register(r'bugs',BugViewSet)
router.register(r'projects',ProjectViewSet)
router.register('users',UserViewSet)