#!/usr/bin/env ipython
import code
import getpass
import sys
import time

# GAE vars
gae_loc = ('/Applications/GoogleAppEngineLauncher.app/Contents/Resources/'
        'GoogleAppEngine-default.bundle/Contents/Resources/google_appengine')
app_id = 'reddit-maze'

# App vars
timeout_backoff = 3 # In seconds
username = None
password = None

# GAE init
sys.path.append(gae_loc)
sys.path.append("%s/lib/yaml/lib"%gae_loc)

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import db
import model

def delete_all(kind_name):
    """Delete all entities of a Kind"""
    kind_class = getattr(model, kind_name)
    k_count = kind_class.all().count()
    done = 0 # Number of deletes pulled off
    err_count = 0 # Concecutive errors
    while k_count > 0:
        # One hit for every 500 and an extra for 1000
        if k_count == 1000:
            hits = 3
        elif k_count > 500:
            hits = 2
        else:
            hits = 1
        print hits,
        sys.stdout.flush()
        while hits > 0:
            try:
                # Do this in one hit to reduce API usage
                db.delete(db.GqlQuery('SELECT __key__ FROM %s'%kind_name).
                                                                fetch(500))
            except KeyboardInterrupt:
                print '\nSTOP!'
                return
            except db.Timeout:
                print 'X',
                err_count += 1
                time.sleep(timeout_backoff*err_count)
            else:
                done += 1
                hits -= 1
                err_count = 0
                print '.',
            sys.stdout.flush()
        print '(%d deleted)'%(done*500)
        k_count = kind_class.all().count()
    print '\nDid %d 500 sized passes'%done

def auth_func():
    global username, password
    if username is None:
        username = raw_input('Username:')
    if password is None:
        password = getpass.getpass('Password:')
    return username, password

host = '%s.appspot.com' % app_id

remote_api_stub.ConfigureRemoteDatastore(app_id, '/remote_api', auth_func,host)
