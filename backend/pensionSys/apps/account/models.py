from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import datetime

class MyUserManager(BaseUserManager):
    def create_user(self, email, created_at, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            created_at=created_at,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,created_at, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            created_at=created_at,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=40,
        unique=True,
    )
    username = models.CharField(
        max_length=40,
        primary_key=True
    )

    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['created_at']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_short_name(self):
        return self.__str__()