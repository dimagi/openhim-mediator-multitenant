import json
from datetime import datetime
from typing import Optional

import requests
from django.conf import settings
from django.http import Http404, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from tenants.models import Tenant, Upstream


@csrf_exempt
def primary_route(request, tenant, upstream, path):
    """
    The mediator forwards the incoming request to the given path at the
    tenant's upstream API.
    """
    tenant = get_object_or_404(Tenant, short_name=tenant)
    upstream = get_upstream_or_404(tenant, upstream, request.method)
    orchestrations = [forward_request_upstream(request, upstream, path)]
    primary_route_response = orchestrations[0]['response']

    data = {
        'x-mediator-urn': settings.MEDIATOR_CONF['urn'],
        'status': 'Successful',
        'response': primary_route_response,
        'orchestrations': orchestrations,
        'properties': {'property': 'Primary Route'},
    }
    return JsonResponse(data, content_type='application/json+openhim')


def forward_request_upstream(request, upstream, path):
    url = slash_join(upstream.base_url, path)
    query_string = request.META['QUERY_STRING']
    body = decode(request.body, request.encoding)
    try:
        data = None
        json_data = json.loads(body)
    except json.JSONDecodeError:
        data = body
        json_data = None
    headers = get_http_headers(request.META)
    request_ts = datetime.utcnow()
    response = requests.request(
        request.method,
        url,
        params=QueryDict(query_string),
        data=data,
        json=json_data,
        headers=headers,
        auth=(upstream.username, upstream.password),
        verify=upstream.verify_cert,
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
            'body': response.text(),
            'timestamp': str(response_ts),
        }
    }


def decode(bytes_: Optional[bytes], encoding: Optional[str]) -> str:
    """
    Returns ``bytes_`` as a string. Decodes using ``encoding`` if given,
    or falls back to ``settings.DEFAULT_CHARSET``.

    Useful for serializing as JSON, because json.dumps() doesn't accept
    bytes.
    """
    if not encoding:
        encoding = settings.DEFAULT_CHARSET
    return bytes_.decode(encoding) if bytes_ else ''


def get_http_headers(request_meta):
    """
    Returns HTTP headers send by the downstream caller.

    Transforms keys to normal HTTP header keys.

    >>> get_http_headers({'HTTP_ACCEPT_LANGUAGE': 'xh', 'SPAM': 'spam'})
    {'Accept-Language': 'xh'}

    """
    headers = {k[5:].replace('_', '-').title(): v
               for k, v in request_meta.items()
               if k.startswith('HTTP_')}
    if request_meta.get('CONTENT_TYPE'):
        headers['Content-Type'] = request_meta['CONTENT_TYPE']
    if request_meta.get('CONTENT_LENGTH'):
        headers['Content-Length'] = request_meta['CONTENT_LENGTH']
    # Drop headers added by OpenHIM
    headers.pop('X-Forwarded-For', None)
    headers.pop('X-Forwarded-Host', None)
    headers.pop('X-Openhim-Transactionid', None)
    return headers


def drop_cookies(headers):
    # openhim-core-js src/middleware/router.js setCookiesOnContext does
    # not accept the cookie format used here. For now, just drop the
    # Set-Cookie header
    headers.pop('Set-Cookie', None)
    return headers


def slash_join(*args: str) -> str:
    """
    Joins arguments with a single ``/``. Useful for concatenating
    strings to form a URL.

    >>> slash_join('https://example.com/', '/foo')
    'https://example.com/foo'
    >>> slash_join('https://example.com', 'api/', '/resource-type/')
    'https://example.com/api/resource-type/'

    """
    if not args:
        return ''
    append_slash = args[-1].endswith('/')
    joined = '/'.join([arg.strip('/') for arg in args])
    return joined + '/' if append_slash else joined


def get_upstream_or_404(
        tenant: Tenant,
        short_name: str,
        method: str,
) -> Upstream:
    """
    Filters Upstream instances by the given ``tenant``, ``short_name``
    and HTTP ``method``. Raises ``Http404`` if there isn't exactly one
    result.
    """
    upstreams = Upstream.objects.filter(
        tenant=tenant,
        short_name=short_name,
    ).all()
    upstreams = [u for u in upstreams
                 if not u.http_methods or method in u.http_methods]
    if len(upstreams) == 1:
        return upstreams[0]
    raise Http404('Unable to find an Upstream matching the given query.')
