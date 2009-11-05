from google.appengine.ext import db

class Tile(db.Model):
    x = db.IntergerProperty(required=True)
    y = db.IntergerProperty(required=True)
    view_blob = db.Blob(required=True)

class Avatar(db.Model):
    x = db.IntergerProperty(required=True)
    y = db.IntergerProperty(required=True)
    name = db.String(required=True)
