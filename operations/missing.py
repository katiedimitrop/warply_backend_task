from tornado.web import Application, RequestHandler
import settings
import json
from pyroaring import BitMap
import csv
import datetime
class Missing(RequestHandler): 
  def get(self,days):
     with open('session_logs.csv', 'r', newline='') as file:
        file_reader = csv.reader(file, delimiter=',')
        reader = csv.reader(file)
        missing_counter = 0

        for row in file_reader:
            
            session_date_time_str = row[1]
            session_date_time_obj = datetime.datetime.strptime(session_date_time_str, '%Y-%m-%d %H:%M:%S')
            date_time_now_str = datetime.datetime.now()
            # Get the difference between datetimes (as timedelta)
            dateTimeDifference = date_time_now_str - session_date_time_obj
            print(dateTimeDifference.days)
            if dateTimeDifference.days >= 7:
                missing_counter = missing_counter+1

        self.write({  'Number of missing users in the last '+days+ ' days' : missing_counter })
