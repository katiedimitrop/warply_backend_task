from tornado.web import Application, RequestHandler
import settings
import json
from pyroaring import BitMap

class Intersection(RequestHandler): 
  def post(self):
     bitmaps_metadata = settings.bitmaps_metadata
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
