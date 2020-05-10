from django.contrib import admin
from bug_reporter.models import *
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(Comment)