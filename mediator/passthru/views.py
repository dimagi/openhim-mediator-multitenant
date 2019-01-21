from datetime import datetime

from django.conf import settings
from django.http import JsonResponse


def get_http_headers(request_meta):
    """
    Returns request['META'] HTTP headers with keys transformed to normal
    HTTP header keys.

    >>> get_http_headers({'HTTP_ACCEPT_LANGUAGE': 'xh', 'SPAM': 'spam'})
    {'Accept-Language': 'xh'}

    """
    headers = {k[5:].replace('_', '-').title(): v for k, v in request_meta.items() if k.startswith('HTTP_')}
    if 'CONTENT_TYPE' in request_meta:
        headers['Content-Type'] = request_meta['CONTENT_TYPE']
    if 'CONTENT_LENGTH' in request_meta:
        headers['Content-Length'] = request_meta['CONTENT_LENGTH']
    return headers


def get_body_string(request):
    """
    Return request body as a string (as opposed to bytes
    """
    return request.body.decode(request.encoding) if request.body else ''


# Extend the mediator by adding more routes/views
def primary_route(request):
    """
    The passthrough mediator forwards the incoming request unchanged
    """
    # Extend the route by building out more complex orchestrations
    orchestrations = [{
        'name': 'Primary Route',
        'request': {
            'method': request.method,
            'headers': get_http_headers(request.META),
            'body': get_body_string(request),
            'timestamp': str(datetime.utcnow()),
            'path': request.path,
            'querystring': request.META['QUERY_STRING'],
        },
        'response': {
            'status': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': 'Primary Route Reached',
            'timestamp': str(datetime.utcnow()),
        }
    }]

    primary_route_response = {
        'status': 200,
        'headers': {'content-type': 'application/json'},
        'body': 'Primary Route Reached',
        'timestamp': str(datetime.utcnow()),
    }
    data = {
        'x-mediator-urn': settings.MEDIATOR_CONF['urn'],
        'status': 'Successful',
        'response': primary_route_response,
        'orchestrations': orchestrations,
        'properties': {'property': 'Primary Route'},
    }
    return JsonResponse(data, content_type='application/json+openhim')
