from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from tenants.models import validate_http_methods


class TestValidateHTTPMethods(SimpleTestCase):

    def test_empty_value(self):
        validate_http_methods('')

    def test_valid_value(self):
        validate_http_methods('POST')

    def test_lower_value(self):
        validate_http_methods('get')

    def test_valid_values(self):
        validate_http_methods('GET POST PUT')

    def test_lower_values(self):
        validate_http_methods('options patch')

    def test_invalid_value(self):
        with self.assertRaises(ValidationError):
            validate_http_methods('OPTION')

    def test_invalid_values(self):
        with self.assertRaises(ValidationError):
            validate_http_methods('CREATE UPDATE')

    def test_comma_separator(self):
        with self.assertRaises(ValidationError):
            validate_http_methods('GET,POST')

    def test_comma_space_separator(self):
        with self.assertRaises(ValidationError):
            validate_http_methods('GET, POST')
