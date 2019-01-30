import json
from datetime import datetime

import requests
from django.conf import settings
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt


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


def drop_cookies(headers):
    # openhim-core-js src/middleware/router.js setCookiesOnContext does
    # not accept the cookie format used here. For now, just drop the
    # Set-Cookie header
    headers.pop('Set-Cookie', None)
    return headers


def forward_request_upstream(request):
    upstream_url = settings.MEDIATOR_CONF['config']['upstreamUrl']
    upstream_username = settings.MEDIATOR_CONF['config']['upstreamUsername']
    upstream_password = settings.MEDIATOR_CONF['config']['upstreamPassword']

    url = '/'.join((upstream_url.rstrip('/'), request.path.lstrip('/')))
    query_string = request.META['QUERY_STRING']
    body = request.body.decode(request.encoding) if request.body else ''
    try:
        data = None
        json_data = json.loads(body)
    except json.JSONDecodeError:
        data = body
        json_data = None
    headers = get_http_headers(request.META)
    request_ts = datetime.utcnow()
    response = requests.request(
        request.method.lower(),
        url,
        params=QueryDict(query_string),
        data=data,
        json=json_data,
        headers=headers,
        auth=(upstream_username, upstream_password)
    )
    response_ts = datetime.utcnow()

    return {
        'name': 'Primary Route',
        'request': {
            'method': request.method,
            'headers': headers,
            'body': body,
            'timestamp': str(request_ts),
            'path': request.path,
            'querystring': query_string,
        },
        'response': {
            'status': response.status_code,
            'headers': drop_cookies(dict(response.headers)),
            'body': response.content.decode(response.encoding),
            'timestamp': str(response_ts),
        }
    }


# Extend the mediator by adding more routes/views
@csrf_exempt
def primary_route(request):
    """
    The passthrough mediator forwards the incoming request unchanged
    """
    # Extend the route by building out more complex orchestrations
    orchestrations = [forward_request_upstream(request)]
    primary_route_response = orchestrations[0]['response']

    data = {
        'x-mediator-urn': settings.MEDIATOR_CONF['urn'],
        'status': 'Successful',
        'response': primary_route_response,
        'orchestrations': orchestrations,
        'properties': {'property': 'Primary Route'},
    }
    return JsonResponse(data, content_type='application/json+openhim')
