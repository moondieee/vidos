from django.contrib.auth.models import UserManager


class UserManager(UserManager):
    def create_superuser(self, *args, **kwargs):
        user = super().create_superuser(*args, **kwargs)
        user.role = 'ADMIN'
        user.save()
