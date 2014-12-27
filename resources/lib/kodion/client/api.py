import json

__author__ = 'bromix'

import urllib
import urllib2
from StringIO import StringIO
import gzip


def _request(method, url, params=None, data=None, headers=None):
    if not headers:
        headers = {}
        pass
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    query = ''
    if params:
        query = urllib.urlencode(params)
        pass
    if query:
        url += '?%s' % query
        pass
    request = urllib2.Request(url)
    if headers:
        for key in headers:
            request.add_header(key, headers[key])
            pass
        pass
    if data:
        if headers.get('Content-Type', '').startswith('application/x-www-form-urlencoded'):
            request.data = urllib.urlencode(data)
            pass
        elif headers.get('Content-Type', '').startswith('application/json'):
            request.data = json.dumps(data)
            pass
        else:
            request.data = urllib.urlencode(data)
            pass
        pass
    request.get_method = lambda: method
    try:
        response = opener.open(request)
    except urllib2.HTTPError, e:
        connection = e
        pass

    if response.headers.get('Content-Encoding', '').startswith('gzip'):
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        response.text = f.read()
        pass
    else:
        response.text = response.read()

    return response


def get(url, params=None, headers=None):
    return _request('GET', url, params=params, headers=headers)


def post(url, params=None, data=None, headers=None):
    if not data:
        data = 'null'
        pass
    return _request('POST', url, params=params, data=data, headers=headers)


def put(url, params=None, data=None, headers=None):
    return _request('PUT', url, params=params, data=data, headers=headers)


def delete(url, params=None, data=None, headers=None):
    return _request('DELETE', url, params=params, data=data, headers=headers)
