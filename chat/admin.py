from django.contrib import admin
from .models import *

# Register your models here.


class DirectMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'message', 'is_read']


admin.site.register(DirectMessage, DirectMessageAdmin)