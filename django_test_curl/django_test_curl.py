import argparse
import base64
import shlex
from urllib.parse import urlparse

from django.http import HttpResponse
from django.test import Client as BaseClient


curl_parser = argparse.ArgumentParser('Dummy curl parser')
curl_parser.add_argument('url')
curl_parser.add_argument('-X', '--request')
curl_parser.add_argument('-v', '--verbose', action='store_true')
curl_parser.add_argument('-I', '--head', action='store_true')
curl_parser.add_argument('-H', '--header', action='append')
curl_parser.add_argument('-d', '--data')


class CurlClientMixin:
    def curl(self, cmd: str) -> HttpResponse:
        """
        Use curl syntax to do a test client request

        Parameters
        ----------
        cmd
            The full curl command, including ``curl``. The scheme and host
            don't matter.

        Returns
        -------
        HttpResponse
        """
        curl_cmd, *args = shlex.split(cmd)
        assert curl_cmd == 'curl'
        opts = curl_parser.parse_args(args)

        if opts.data and not opts.request:
            opts.request = 'post'
        if opts.head and not opts.request:
            opts.request = 'head'
        if not opts.request:
            opts.request = 'get'
        assert opts.request in ('head', 'delete', 'get', 'post')

        url = urlparse(opts.url)

        kwargs = {}

        if url.username and url.password:
            hashcode = base64.b64encode(f'{url.username}:{url.password}'.encode('utf-8'))
            kwargs['HTTP_AUTHORIZATION'] = f'Basic {hashcode.decode("utf8")}'

        header_items = [x.split(':', 2) for x in opts.header or []]
        headers = {'HTTP_' + k.strip().upper().replace('-', '_'): v.strip()
                   for k, v in header_items}
        if 'HTTP_CONTENT_TYPE' in headers:
            kwargs['content_type'] = headers.pop('HTTP_CONTENT_TYPE')

        if opts.data:
            kwargs['data'] = opts.data

        return getattr(self, opts.request)(url.path, **headers, **kwargs)


class CurlClient(CurlClientMixin, BaseClient):
    pass
