from google.appengine.ext import db

class Tile(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    view_blob = db.BlobProperty(required=True)

class Avatar(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
