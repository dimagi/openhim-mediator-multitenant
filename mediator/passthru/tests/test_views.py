import doctest
from collections import namedtuple
from copy import copy
from unittest.mock import patch

from django.conf import settings
from django.http import QueryDict
from django.test import SimpleTestCase, Client, override_settings

import passthru.views


Response = namedtuple('Response', 'status_code headers content encoding')
mediator_conf = copy(settings.MEDIATOR_CONF)
mediator_conf['config'] = {
    'upstreamUrl': "https://play.dhis2.org/2.31.0/",
    'upstreamUsername': 'admin',
    'upstreamPassword': 'district',
}


@override_settings(MEDIATOR_CONF=mediator_conf)
class PrimaryRouteTests(SimpleTestCase):

    def setUp(self):
        self.response = Response(
            status_code=200,
            headers={'content-type': 'application/json'},
            content=b'Primary Route Reached',
            encoding='UTF-8'
        )

    def test_request(self):
        with patch('passthru.views.requests.request') as request_mock:
            request_mock.return_value = self.response

            client = Client()
            client.get('/api/resources')
            request_mock.assert_called_with(
                'get',
                'https://play.dhis2.org/2.31.0/api/resources',
                auth=('admin', 'district'),
                data='',
                headers={'Cookie': ''},
                json=None,
                params=QueryDict({})
            )

    def test_response(self):
        # Sample response:
        #     {
        #         'x-mediator-urn': 'urn:uuid:01234567-89ab-cdef-0123-456789abcdef',
        #         'status': 'Successful',
        #         'response': {
        #             'status': 200,
        #             'headers': {'content-type': 'application/json'},
        #             'body': 'Primary Route Reached',
        #             'timestamp': '2019-01-21 16:49:13.031168'
        #         },
        #         'orchestrations': [{
        #             'name': 'Primary Route',
        #             'request': {
        #                 'method': 'GET',
        #                 'headers': {'Cookie': ''},
        #                 'body': '',
        #                 'timestamp': '2019-01-21 16:49:13.031158',
        #                 'path': '/',
        #                 'querystring': ''
        #             },
        #             'response': {
        #                 'status': 200,
        #                 'headers': {'Content-Type': 'application/json'},
        #                 'body': 'Primary Route Reached',
        #                 'timestamp': '2019-01-21 16:49:13.031166'
        #             }
        #         }],
        #         'properties': {'property': 'Primary Route'}
        #     }
        with patch('passthru.views.requests.request') as request_mock:
            request_mock.return_value = self.response

            client = Client()
            response = client.get('/api/resources')
            data = response.json()

        self.assertEqual(response.status_code, 200)
        for key in ('x-mediator-urn', 'status', 'response', 'orchestrations', 'properties'):
            self.assertIn(key, data)
        self.assertEqual(data['x-mediator-urn'], settings.MEDIATOR_CONF['urn'])
        self.assertEqual(data['status'], 'Successful')
        self.assertEqual(data['response']['status'], 200)
        self.assertEqual(len(data['orchestrations']), 1)
        self.assertEqual(data['orchestrations'][0]['name'], 'Primary Route')
        self.assertEqual(data['properties']['property'], 'Primary Route')


class DocTests(SimpleTestCase):

    def test_doctests(self):
        results = doctest.testmod(passthru.views)
        self.assertEqual(results.failed, 0)
