Django test curl
================

[![Build Status](https://travis-ci.org/crccheck/django-test-curl.svg?branch=master)](https://travis-ci.org/crccheck/django-test-curl)

With _Django test curl_, you can take your test cases and immediately try them
against an actual server via the magic of copy-paste!

Django's [testing tools] come with a great [test client] you can use to
simulate requests against views. Against deployed Django projects, if you want
to do simple requests, you would probably use [curl]. If you want to use the
same syntax to do both, this is the package for you.

### Good places to use this

This was developed to TDD recreating an existing API. If you have a library of
curl requests that you need to replicate, this is perfect for that. If you need
a portable format to turn test cases into QA automation, this is great for
that.

### Bad places to use this

If the `curl` syntax requires lots of string formatting, you should stick to
the traditional [test client]. If the test case isn't copy-pastable, it's not a
good fit. This also means if you use randomness to generate your requests,
you'll lose that extra test coverage.


Installation
------------

```sh
$ pip install django-test-curl
```


Usage
-----

```python
from django_test_curl import CurlClient

class SimpleTest(TestCase):
    """https://docs.djangoproject.com/en/stable/topics/testing/tools/#example"""
    def setUp(self):
        self.client = CurlClient()

    def test_details(self):
        response = self.client.curl("""
          curl http://localhost:8000/customer/details/
        """)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['customers']), 5)
```

If you're using a custom `Client`, you can use the mixin version:

```
from django.test import Client
from django_test_curl import CurlClientMixin

class MyClient(CurlClientMixin, Client):
    ...
```

We support a subset of curl's functionality. For a full list and examples, see
the [tests](./django_test_curl/test_django_test_curl.py).

* Headers
* GET/POST/PUT/DELETE/etc
* HTTP basic auth


[curl]: https://curl.haxx.se/
[test client]: https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client
[testing tools]: https://docs.djangoproject.com/en/stable/topics/testing/tools/
