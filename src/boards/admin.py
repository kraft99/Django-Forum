from django.contrib import admin
from .import models
# Register your models here.


admin.site.register(models.Board)
admin.site.register(models.Topic)
admin.site.register(models.Post)

