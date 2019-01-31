from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Tenant(models.Model):
    short_name = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200)


class Upstream(models.Model):
    """
    An API upstream of this mediator. e.g. DHIS2 or OpenMRS
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    short_name = models.SlugField(max_length=200, db_index=True)
    base_url = models.URLField()
    verify_cert = models.BooleanField(default=True)
    username = models.CharField(max_length=200)
    # NOTE: If settings.SECRET_KEY is changed, passwords cannot be decrypted
    _password = models.CharField(max_length=200)

    @property
    def password(self):
        cipher_suite = Fernet(settings.SECRET_KEY)
        plaintext_bytes = cipher_suite.decrypt(self._password)
        return plaintext_bytes.decode('utf8')

    @password.setter
    def password(self, plaintext):
        cipher_suite = Fernet(settings.SECRET_KEY)
        plaintext_bytes = plaintext.encode('utf8')
        self._password = cipher_suite.encrypt(plaintext_bytes)


class TenantUser(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)  # Superusers do not have a Tenant
