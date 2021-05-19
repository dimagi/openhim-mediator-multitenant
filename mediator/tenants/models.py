import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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
    http_methods = models.CharField(max_length=200, default='', blank=True,
                                    validators=[validate_http_methods])
    verify_cert = models.BooleanField(default=True)
    username = models.CharField(max_length=200, blank=True)
    # NOTE: If settings.SECRET_KEY is changed, passwords cannot be decrypted
    _password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        if self.http_methods:
            return f'{self.short_name} ({self.http_methods})'
        else:
            return str(self.short_name)

    def save(self, *args, **kwargs):
        self.http_methods = self.http_methods.upper()
        super().save(*args, **kwargs)

    @property
    def password(self):
        if not self._password:
            return ''
        key = get_fernet_key()
        fernet = Fernet(key)
        base64_bytes = self._password.encode('ascii')
        plaintext_bytes = fernet.decrypt(base64_bytes)
        return plaintext_bytes.decode('utf8')

    @password.setter
    def password(self, plaintext):
        key = get_fernet_key()
        fernet = Fernet(key)
        plaintext_bytes = plaintext.encode('utf8')
        base64_bytes = fernet.encrypt(plaintext_bytes)
        self._password = base64_bytes.decode('ascii')


class TenantUser(AbstractUser):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,  # Superusers do not have a Tenant
    )


def get_fernet_key() -> bytes:
    salt = b'openhim-mediator-multitenant---'  # Can't be random
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    secret_key = settings.SECRET_KEY.encode('ascii')
    return base64.urlsafe_b64encode(kdf.derive(secret_key))
