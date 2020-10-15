from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from pyroaring import BitMap
import json

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

def make_app():
 #route endpoints to classes
  urls = [
    ("/", Bitmaps),
    (r"/api/bitmap/([^/]+)?", Bitmap),
    (r"/api/union/", Union),
    (r"/api/intersection/", Intersection)
  ]
  return Application(urls, debug=True)
  
if __name__ == '__main__':
  app = make_app()
  app.listen(3000)
  IOLoop.instance().start()