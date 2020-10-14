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
  def get(self,id):
    global bitmaps_metadata
    if len(bitmaps_metadata) > int(id):
        self.write({  'BitMap with id %s' % id : bitmaps_metadata[int(id)] })
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})

  def post(self, _):
    global bitmaps_metadata
    #on post request create a bitmap and add to collection
    json_data = json.loads(self.request.body)
    json_data["id"] = len(bitmaps_metadata)
   #remove duplicates
    json_data["set"] = sorted(list(set(json_data["set"])))
    bitmaps_metadata.append(json_data)
    #bm = BitMap(bitmaps_metadata[0]["set"])
    #print(bm.to_array().tolist())
    self.write({'message': 'new Bitmap with id %s added' % str(len(bitmaps_metadata)-1)})

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
                bitmaps_metadata[index]["set"] = sorted(list(set(json_data["set"])))
         
                self.write({'message': 'BitMap with id %s was updated' % id})
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})

class Union(RequestHandler): 
  def post(self):
     global bitmaps_metadata
     json_data = json.loads(self.request.body)
     pairs = json_data.items()
     ids = []
     #isolate ids of bitmaps to union
     for key, value in pairs:
        ids.append(value)
                 
     bm_union = BitMap()
     #calculate union of all specified bitmaps
     for bm_id in ids:
        current_bm = BitMap(bitmaps_metadata[bm_id]["set"])
        bm_union = BitMap.union(bm_union,current_bm)

     self.write({  'Bitmap ids' : ids })
     self.write({  'Bitmap union ': bm_union.to_array().tolist() })
        
class Intersection(RequestHandler): 
  def post(self):
     global bitmaps_metadata
     json_data = json.loads(self.request.body)
     pairs = json_data.items()
     ids = []
     #isolate ids of bitmaps for intersection
     for key, value in pairs:
        ids.append(value)
                 

     #calculate intersection of all specified bitmaps
     bm_intersection = BitMap()
     
     for previous, current in zip(ids, ids[1:]):
        previous_bm = BitMap(bitmaps_metadata[previous]["set"])
        current_bm = BitMap(bitmaps_metadata[current]["set"])
        if len(bm_intersection.to_array().tolist()) == 0:
            bm_intersection = BitMap.intersection(previous_bm,current_bm)
        else:
            bm_intersection = BitMap.intersection(bm_intersection,previous_bm,current_bm)

     self.write({  'Bitmap ids' : ids })
     self.write({  'Bitmap intersection ': bm_intersection.to_array().tolist() })


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