from tornado.web import Application, RequestHandler
import settings
import json
from pyroaring import BitMap

class Union(RequestHandler): 
  def post(self):
     bitmaps_metadata = settings.bitmaps_metadata
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
