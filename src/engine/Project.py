from Module import Module
from Location import Location


class Project():
    def __init__(self, name, method, date):
        self.name = name
        self.development_method = method
        self.delivery_date = date
        self.modules = list()
        self.locations = list()
