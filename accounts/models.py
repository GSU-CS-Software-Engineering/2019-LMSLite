from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


from courses.models import Course


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False, role=None):

        if not email:
            raise ValueError("Please input valid email")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            role=1
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
            role=0
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USER_TYPE_CHOICES = (
        (2, 'student'),
        (1, 'professor'),
        (0, 'admin'),
    )

    role = models.SmallIntegerField(choices=USER_TYPE_CHOICES, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Student(User):
    courses = models.ManyToManyField('courses.Course')

    def __str__(self):
        return self.user.email


class Professor(User):
    courses = models.ManyToManyField('courses.Course')

    def __str__(self):
        return self.user.email

