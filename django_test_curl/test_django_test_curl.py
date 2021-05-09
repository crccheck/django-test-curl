import unittest
from unittest.mock import patch

from . import CurlClient


class CurlTests(unittest.TestCase):
    def setUp(self):
        self.client = CurlClient()

    @patch.object(CurlClient, "get")
    def test_curl_extracts_url(self, mock_req):
        self.client.curl(
            """
            curl http://localhost:8000/api/v1/poop/
            """
        )
        mock_req.assert_called_once_with("/api/v1/poop/")

    @patch.object(CurlClient, "get")
    def test_curl_extracts_quoted_url(self, mock_req):
        self.client.curl(
            """
            curl "http://localhost:8000/api/v1/poop/"
            """
        )
        mock_req.assert_called_once_with("/api/v1/poop/")

    @patch.object(CurlClient, "get")
    def test_curl_extracts_get_params(self, mock_req):
        self.client.curl(
            """
            curl 'http://localhost:8000/api/v1/poop/?foo=a&foo=b'
            """
        )
        mock_req.assert_called_once_with("/api/v1/poop/?foo=a&foo=b")

    @patch.object(CurlClient, "head")
    def test_curl_sees_head_implies_head(self, mock_req):
        self.client.curl(
            """
            curl -I http://localhost:8000/neck-topper
            """
        )
        mock_req.assert_called_once_with("/neck-topper")

    @patch.object(CurlClient, "post")
    def test_curl_sees_data_implies_post(self, mock_req):
        self.client.curl(
            """
            curl -v http://localhost:8000/api/v1/awesome/ \
             -H 'content-type: application/json' \
             -d '{"foo": "bar"}'
            """
        )
        mock_req.assert_called_once()

    @patch.object(CurlClient, "post")
    def test_curl_converts_content_type(self, mock_req):
        self.client.curl(
            """
            curl -v http://localhost:8000/api/v1/awesome/ \
             -H 'content-type: application/json' \
             -d '{"foo": "bar"}'
            """
        )
        mock_req.assert_called_once()
        args, kwargs = mock_req.call_args
        self.assertEqual(args, ("/api/v1/awesome/",))
        self.assertEqual(kwargs["content_type"], "application/json")
        self.assertTrue(kwargs["data"])

    @patch.object(CurlClient, "get")
    def test_curl_converts_auth(self, mock_req):
        self.client.curl(
            """
            curl http://test:pass@localhost:8000/secret/files/
            """
        )
        mock_req.assert_called_once_with(
            "/secret/files/", HTTP_AUTHORIZATION="Basic dGVzdDpwYXNz"
        )
