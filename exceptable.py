from google.appengine.ext import webapp
from google.appengine.runtime import DeadlineExceededError

class HTTPException(Exception):
    pass

class HTTPBadRequest(HTTPException):
    code = 400

class HTTPConflict(HTTPException):
    code = 409

class ExceptableHandler(webapp.RequestHandler):
    def err(self, err_code, err_str):
        self.response.headers['Content-type'] = 'application/json'
        self.error(err_code)
        self.response.out.write({'code':err_code, 'error':err_str})

def exceptable(meth):
    def decorated(self, *args):
        try:
            return meth(self, *args)
        except HTTPException, e:
            self.err(e.code,e.message)
        except DeadlineExceededError, e:
            log.error('DeadlineExceeded!')
            log.exception(e)
            self.err(500,'Sorry... This was killed by App Engine for'
                            'running too long.')
        except db.Timeout, e:
            log.error('Datastore timeout. %s'%e.message)
            log.exception(e)
            self.err(500,'Sorry... the data store timed out')
    return decorated

