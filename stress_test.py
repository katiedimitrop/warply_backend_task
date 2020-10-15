import tornado.ioloop
import tornado.web
import tornado.gen

import math
import random
import json
import datetime

class MainHandler(tornado.web.RequestHandler):
    
    count = 0
    
    @tornado.gen.coroutine
    def get(self):
        seconds_delay = 0.1
        delay = datetime.timedelta(seconds=seconds_delay)
        MainHandler.count+=1
        print (self.count)
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, delay)
        self.finish(json.dumps([x*x for x in range(1000)]))

application = tornado.web.Application([
    (r"/", MainHandler),
], {'debug':True})

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
