from django.db import models
from Users.models import User


class notification(models.Model):
    is_seen = models.BooleanField(default=False)
    title = models.TextField()
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "notification"
