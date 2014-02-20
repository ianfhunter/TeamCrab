from Module import Module
from Location import Location
import datetime

class Project():
    def __init__(self, name, method, date):
        self.name = name
        self.development_method = method
        self.delivery_date = date
        self.modules = list()
        self.locations = list()
        self.start_time = datetime.datetime(2014,1,1,0,0,0)
        self.current_time = datetime.datetime(2014,1,1,0,0,0)