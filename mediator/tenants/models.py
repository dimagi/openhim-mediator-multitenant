from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_http_methods(value: str):
    """
    Validates that ``value`` is a space-separated list of HTTP methods,
    or an empty string to denote all methods.
    """
    if value == '':
        return
    valid = {'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS',
             'TRACE', 'PATCH'}
    values = set(value.upper().split())
    if invalid := values - valid:
        if len(invalid) == 1:
            message = _('%(invalid)s is not a valid HTTP method')
        else:
            message = _('%(invalid)s are not valid HTTP methods')
        raise ValidationError(message, params={'invalid': ','.join(invalid)})


class Tenant(models.Model):
    short_name = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Upstream(models.Model):
    """
    An API upstream of this mediator. e.g. DHIS2 or OpenMRS
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    short_name = models.SlugField(max_length=200, db_index=True)
    base_url = models.URLField()
    # A space-separated list of HTTP methods or an empty string to denote all
    http_methods = models.CharField(max_length=200, default='',
                                    validators=[validate_http_methods])
    verify_cert = models.BooleanField(default=True)
    username = models.CharField(max_length=200)
    # NOTE: If settings.SECRET_KEY is changed, passwords cannot be decrypted
    _password = models.CharField(max_length=200)

    def __str__(self):
        return str(self.short_name)

    def save(self, *args, **kwargs):
        self.http_methods = self.http_methods.upper()
        super().save(*args, **kwargs)

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
