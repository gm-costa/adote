from django.db import models
from django.contrib.auth.models import User


class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64)
    valid = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username
