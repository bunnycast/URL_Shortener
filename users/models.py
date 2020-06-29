from django.db import models


class User(models.Model):
    is_membership = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)