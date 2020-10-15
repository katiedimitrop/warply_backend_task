from tornado.web import Application, RequestHandler
import settings
import json
from pyroaring import BitMap

class Bitmap(RequestHandler):
  def get(self,id):
    bitmaps_metadata = settings.bitmaps_metadata
    if len(bitmaps_metadata) > int(id):
        self.write({  'BitMap with id %s' % id : bitmaps_metadata[int(id)] })
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})

  def post(self, _):
    bitmaps_metadata = settings.bitmaps_metadata
    #on post request create a bitmap and add to collection
    json_data = json.loads(self.request.body)
    json_data["id"] = len(bitmaps_metadata)
   #remove duplicates
    json_data["set"] = sorted(list(set(json_data["set"])))
    settings.bitmaps_metadata.append(json_data)
    #bm = BitMap(bitmaps_metadata[0]["set"])
    #print(bm.to_array().tolist())
    self.write({'message': 'new Bitmap with id %s added' % str(len(bitmaps_metadata)-1)})

  def delete(self, id):
    #keyword necessary to access global items
    bitmaps_metadata = settings.bitmaps_metadata
    if len(bitmaps_metadata) > int(id):
    #remove bitmap from collection by id
        new_bms = [bm for bm in bitmaps_metadata if bm['id'] is not int(id)]
        bitmaps_metadata = new_bms
        settings.bitmaps_metadata = bitmaps_metadata
        self.write({'message': 'BitMap with id %s was deleted' % id})
        
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})

  def put(self, id):
  #keyword necessary to access global items
    bitmaps_metadata = settings.bitmaps_metadata
    if len(bitmaps_metadata) > int(id):
        json_data = json.loads(self.request.body)
        for index,bm in enumerate(bitmaps_metadata):
            if int(bm['id']) is int(id):
                bitmaps_metadata[index]["set"] = sorted(list(set(json_data["set"])))
         
                self.write({'message': 'BitMap with id %s was updated' % id})
    else:
        self.write({'message': 'BitMap with id %s does not exist' % id})
