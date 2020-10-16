from tornado.web import *
from tornado.ioloop import IOLoop
import tornado
from pyroaring import BitMap
import json
import re
import datetime
import csv
import random

#my own classes
import settings
from bitmap import Bitmap
from operations.intersection import Intersection
from operations.union import Union
from operations.missing import Missing


settings.init()          # Call only once
#collection of all user-created bitmaps since server initialization
bitmaps_metadata = settings.bitmaps_metadata
tags = ["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8","tag9","tag10"]
#1000
users = []
#1000x10
user_tags=[]
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

        if (given_name not in users):
            #update lists with new user
            users.append(given_name)
            
            #randomly generate user tags
            noOfTags = random.randint(1,10)
            userTagList = []
            for i in range(0,noOfTags):
                randomTag = random.sample(tags,1)
                userTagList.append(randomTag[0])
        
                #print(userTagList)

            #update list with new user
            user_tags.append(userTagList)

            #update csv with new user 

            with open('users.csv', 'a', newline='') as file:
                file_writer = csv.writer(file,quotechar = "'")             
                file_writer.writerow(['\"'+given_name+'\"'])

            with open('user_tags.csv', 'a', newline='') as file:
                file_writer = csv.writer(file,delimiter=",",quotechar = "'")
                print(userTagList) 
                file_writer.writerow(userTagList)

        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        user = str(self.get_secure_cookie("user"), 'utf-8')
        now = datetime.datetime.now()
        #print ("Current date and time : ")
        #print (now.strftime("%Y-%m-%d %H:%M:%S"))
        #print("LOGGED OUT USER %s" % user)

        
        with open('session_logs.csv', 'a', newline='') as file:
            file_writer = csv.writer(file, delimiter=',',quotechar = "'")
            file_writer.writerow([ user, now.strftime('\"%Y-%m-%d %H:%M:%S\"') ])

        
        self.clear_cookie("user")
        self.redirect("/")

class NoOfUsersWithTags(BaseHandler):
    def post(self):
        tagA = json.loads(self.request.body)["tagA"]
        tagB = json.loads(self.request.body)["tagB"] 
        user_counter = 0
        for taglist in user_tags:
            if (tagA in taglist) and (tagB in taglist):
                user_counter=user_counter+1
        self.write("Number of users with %s and %s is %d" % (tagA,tagB,user_counter))
        
class UsersWithTag(BaseHandler):
    def post(self):
        tagA = json.loads(self.request.body)["tagA"]
        users_with_tag = []
        for user_index,user in enumerate(users):
            if tagA in user_tags[user_index]:
                users_with_tag.append(user)
        self.write(''+str(users_with_tag))

def make_app():
 #route endpoints to classes
  urls = [
     
    (r"/", MainHandler),
    (r"/api/bitmaps/?", Bitmaps),
    (r"/api/bitmap/([^/]+)?", Bitmap),
    (r"/api/union/?", Union),
    (r"/api/intersection/?", Intersection),
    (r'/api/login/?', LoginHandler),
    (r'/api/logout/?', LogoutHandler),
    (r'/api/noOfMissingUsers/([^/]+)?', Missing),
    (r'/api/noOfUsersWithTags/?', NoOfUsersWithTags),
    (r'/api/usersWithTag/?', UsersWithTag)
  ]

  #read users and their tags from csv


  with open('users.csv', mode='r', encoding='utf-8-sig') as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            users.append(row)

            
  with open('user_tags.csv', mode='r', encoding='utf-8-sig') as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            temp_tag_list = []
            for tag in row:         
                temp_tag_list.append(tag)
            user_tags.append(temp_tag_list)    
  
  
  return Application(urls, debug=True,xsrf_cookies= False, cookie_secret= "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url= "/api/login/?")
  
if __name__ == '__main__':
  settings.app = make_app()
  settings.app.listen(3000)
  IOLoop.instance().start()
   