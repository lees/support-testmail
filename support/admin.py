from django.contrib import admin
from support.models import Issue

class IssueAdmin(admin.ModelAdmin):
    pass
admin.site.register(Issue, IssueAdmin)
