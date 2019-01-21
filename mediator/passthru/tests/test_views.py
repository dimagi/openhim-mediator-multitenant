import doctest

from django.conf import settings
from django.test import TestCase, SimpleTestCase, Client

import passthru.views


class PrimaryRouteTests(TestCase):

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
        client = Client()
        response = client.get('/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        for key in ('x-mediator-urn', 'status', 'response', 'orchestrations', 'properties'):
            self.assertIn(key, data)
        self.assertEqual(data['x-mediator-urn'], settings.MEDIATOR_CONF['urn'])
        self.assertEqual(data['status'], 'Successful')
        self.assertEqual(len(data['orchestrations']), 1)
        self.assertEqual(data['orchestrations'][0]['name'], 'Primary Route')
        self.assertEqual(data['properties']['property'], 'Primary Route')


class DocTests(SimpleTestCase):

    def test_doctests(self):
        results = doctest.testmod(passthru.views)
        self.assertEqual(results.failed, 0)
