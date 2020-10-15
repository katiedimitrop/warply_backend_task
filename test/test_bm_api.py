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


#class TestCase(AsyncTestCase):
 #   @tornado.testing.gen_test
  #  def test_1000_concurrent_sessions(self):
   #     client = AsyncHTTPClient()
    #    post_body = str(urllib.parse.urlencode({"name":"testName"}))
        #Send http post request on login
     #   response = yield client.fetch("http://localhost:3000/api/login/",method="POST", body=post_body)
      #  # Test contents of response
       # self.assertEqual(response.code, 200)        
  

# This test uses argument passing between self.stop and self.wait.
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        client.fetch("http://www.tornadoweb.org/", self.stop)
        response = self.wait()
        # Test contents of response
        self.assertIn("FriendFeed", response.body)
     