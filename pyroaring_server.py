from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from pyroaring import BitMap
import json

#collection of all user-created bitmaps since server initialization

bitmaps_metadata = []

class Bitmaps(RequestHandler):
#on get request display all the bitmaps 
  def get(self):
    self.write({'bitmaps': bitmaps_metadata})

class Bitmap(RequestHandler):
  def post(self, _):
    global bitmaps_metadata
    #on post request create a bitmap and add to collection
    json_data = json.loads(self.request.body)
    json_data["id"] = len(bitmaps_metadata)
   #remove duplicates
    json_data["set"] = list(set(json_data["set"]))
    bitmaps_metadata.append(json_data)
    #bm = BitMap(bitmaps_metadata[0]["set"])
    #print(bm.to_array().tolist())
    self.write({'message': 'new Bitmap added'})

  def delete(self, id):
    #keyword necessary to access global items
    global bitmaps_metadata
    if len(bitmaps_metadata) > int(id):
    #remove bitmap from collection by id
        new_bms = [bm for bm in bitmaps_metadata if bm['id'] is not int(id)]
        bitmaps_metadata = new_bms
        self.write({'message': 'BitMap with id %s was deleted' % id})
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})

  def put(self, id):
    #keyword necessary to access global items
    global bitmaps_metadata
    if len(bitmaps_metadata) > int(id):
        json_data = json.loads(self.request.body)
        for index,bm in enumerate(bitmaps_metadata):
            if int(bm['id']) is int(id):
                bitmaps_metadata[index]["set"] = list(set(json_data["set"]))
         
                self.write({'message': 'BitMap with id %s was updated' % id})
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})

def make_app():
  #route endpoints to classes
  urls = [
    ("/", Bitmaps),
    (r"/api/bitmap/([^/]+)?", Bitmap)
  ]
  return Application(urls, debug=True)
  
if __name__ == '__main__':
  app = make_app()
  app.listen(3000)
  IOLoop.instance().start()