from django.contrib import admin
from bug_reporter.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(Comment)