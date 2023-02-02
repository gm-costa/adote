from django.contrib import admin
from .models import ResetPassword


class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'valid')

admin.site.register(ResetPassword, ResetPasswordAdmin)
