from django.contrib import admin

from .models import *
admin.site.register(User)
admin.site.register(UserGroup)
admin.site.register(Problem)
admin.site.register(TestSet)
admin.site.register(Test)
admin.site.register(Task)
admin.site.register(Submission)
admin.site.register(Tag)
admin.site.register(Announcement)
