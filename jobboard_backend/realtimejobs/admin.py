from django.contrib import admin
from .models import JobPost, Tag, JobInteraction, User, Company, JobAlert, Category, JobType


admin.site.register(JobPost)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(JobInteraction)
admin.site.register(Company)
admin.site.register(JobAlert)
admin.site.register(Category)
admin.site.register(JobType)
