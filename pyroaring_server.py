from tornado.web import *
from tornado.ioloop import IOLoop
import tornado
from pyroaring import BitMap
import json
import re
#my own classes
import settings
from bitmap import Bitmap
from operations.intersection import Intersection
from operations.union import Union

settings.init()          # Call only once
#collection of all user-created bitmaps since server initialization
bitmaps_metadata = settings.bitmaps_metadata

class Bitmaps(RequestHandler):
#on get request display all the bitmaps 
  def get(self):
    bitmaps_metadata = settings.bitmaps_metadata
    self.write({'bitmaps': bitmaps_metadata})


#You can require that the user be logged in using the Python decorator
#tornado.web.authenticated. If a request goes to a method with this decorator,
#and the user is not logged in, they will be redirected to login_url
#(another application setting).

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):

    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>'
                    'Log in with a name at http://localhost:3000/api/login')
    def post(self):
        
        given_name = json.loads(self.request.body)["name"] 
        self.set_secure_cookie("user",given_name )
        #print("%r %s " % (self.request, self.request.body.decode()))
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

def make_app():
 #route endpoints to classes
  urls = [
     
    (r"/", MainHandler),
    (r"/api/bitmaps/?", Bitmaps),
    (r"/api/bitmap/([^/]+)?", Bitmap),
    (r"/api/union/?", Union),
    (r"/api/intersection/?", Intersection),
    (r'/api/login/?', LoginHandler),
    (r'/api/logout/?', LogoutHandler)
  ]
 
  return Application(urls, debug=True,xsrf_cookies= False, cookie_secret= "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url= "/api/login/?")
  
if __name__ == '__main__':
  settings.app = make_app()
  settings.app.listen(3000)
  IOLoop.instance().start()