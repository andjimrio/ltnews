from django.contrib import admin
from news import models

admin.site.register(models.Profile)
admin.site.register(models.Section)
admin.site.register(models.Feed)
admin.site.register(models.Item)
admin.site.register(models.Status)
admin.site.register(models.Keyword)
admin.site.register(models.Comment)
