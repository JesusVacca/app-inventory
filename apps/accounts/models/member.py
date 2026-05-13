from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from apps.common.utils import RoleChoices


class BaseMemberManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role',RoleChoices.Admin)
        return self.create_user(email, password, **extra_fields)


"""
Clase que se converitá en mi modelo en la db (Tabla)
Tiene datos basico para registro de nuevos usuario
Hereda de una clase especial que ayudará con validaciones y encriptamiento de contraseñas
"""
class Member(AbstractBaseUser):
    objects = BaseMemberManager()
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True, unique=True, db_index=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.Cliente,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',]

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff
    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

    def full_name(self):
        return f'{self.first_name} {self.last_name if self.last_name else ""}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'




