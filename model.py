from google.appengine.ext import db
import pickle

class Tile(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    view_blob = db.BlobProperty(required=True)
    def serial(self):
        return pickle.loads(self.view_blob)

class Avatar(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    def __repr__(self):
        return '<Avatar %s (%d,%d)>'%(self.name, self.x, self.y)
    def serial(self):
        return {'name':self.name, 'x':self.x, 'y':self.y}
