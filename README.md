Django test curl
================

Django's [testing tools] come with a test client you can use to simulate
requests against your views. If you ever want to do real-world requests, you'll
probably use [curl]. If you want to use the same syntax to do both, this is the
package for you.


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


[curl]: https://curl.haxx.se/
[testing tools]: https://docs.djangoproject.com/en/stable/topics/testing/tools/
