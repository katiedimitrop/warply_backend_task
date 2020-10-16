import tornado
import urllib
from tornado.testing import AsyncHTTPTestCase, AsyncTestCase, AsyncHTTPClient

# This test uses coroutine style.

class MyTestCase(AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        response = yield client.fetch("http://localhost:3000/api/bitmaps")
        # Test contents of response
        self.assertIn("bitmaps", str(response.body))


      
  
