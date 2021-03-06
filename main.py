#!/usr/bin/env python
import wsgiref.handlers

from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):

  def get(self):
    self.redirect('/static/welcome.html')

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
