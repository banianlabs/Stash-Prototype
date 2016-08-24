#!venv/bin/python

import os
import sys
import json
import argparse
import requests
import time

from stash import app
from stash.core import db
from config import *


# --------- Databases -------------

def create_sample_db_entry(api_endpoint, payload):
    url = os.path.join('http://localhost:5000' + api_endpoint)
    r = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print r.text
    
def create_db():
    db.create_all()

# Will eventually become testing command
def create_test_user():
    from stash.core import db
    from stash.models import user_datastore, User

    # Create fake app context
    with app.app_context():
        user = user_datastore.create_user(
            username="johndoe", 
            email="johndoe@gmail.com",
            password="123"
        )
        db.session.commit()

        fetched_user = User.query.get(user.id)
        if not fetched_user.check_password('123'):
            raise Exception("Password verification failed!")
        else:
            print "Tests check out!"

def drop_db():
    db.drop_all()

def recreate_db():
    drop_db()
    create_db()

# --------- Static Assets ----------

BOOTSTRAP_URL = "https://raw.githubusercontent.com/twbs/bootstrap/master/less/%s"
def download(twbs=None):
    if twbs:
        src = BOOTSTRAP_URL % twbs
        less_path = os.path.join("stash", LESS_CONFIG['SRC'])
        dst = os.path.join(less_path, twbs)
        r = requests.get(src)
        if r.status_code == 200:
            out = open(dst, 'w')
            out.write(r.text)
            out.close()
            print "Done!"
        else:
            print "Error! Not fetched. Check that the file " + twbs + " is available at "
            print src

def watch():
    # Recompile
    src = os.path.join("stash", LESS_CONFIG['SRC'])
    dst = os.path.join("stash", LESS_CONFIG['DST'])
    src_file = os.path.join("stash", LESS_CONFIG['SRC_FILE'])
    dst_file = os.path.join("stash", LESS_CONFIG['DST_FILE'])

    print "Watching %s and recompiling to %s" % (src, dst)
    now = time.time()
    before = dict([(f, now) for f in os.listdir(src)])
    last_updated = now
    while 1:
        time.sleep(1)
        now = time.time()
        after = dict([(f, now) for f in os.listdir(src)])
        added   = [f for f in after if not f in before]
        updated = [f for f in after if f in before and 
            os.stat(os.path.join(src, f)).st_mtime > last_updated]
        removed = [f for f in before if f not in after]
        if len(added) > 0 or len(updated) > 0 or len(removed) > 0:
            os.system("lessc %s %s" % (src_file, dst_file))
            print "recompiled less"
            before = after
            last_updated = now



# -------- Flask / Server -----------
def serve():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# -------- Commands Interface --------

# List of commands. When adding new one, put
# the command name in here and index into this 
# array when parsing within main
Commands = [
    "create_db",
    "delete_db",
    "seed_db",
    "watcher",
    "fetch",
    "server",
    "recreate_db",
    "create_test_user",
]
def print_cmds():
    for cmd in Commands:
        print cmd

def generate_list_of_commands():
    return "Available commands:\n" + (",".join(Commands))

def main():
    parser = argparse.ArgumentParser(description='Manage this Flask application.', epilog=generate_list_of_commands())
    parser.add_argument('command', help='the name of the command you want to run')
    parser.add_argument('--data', help='the file with data for seeding the database')
    parser.add_argument('--twbs', help='when getting bootstrap files, specify the filename')
    args = parser.parse_args()

    if args.command == Commands[0]:
        create_db()

        print "DB created!"


    elif args.command == Commands[1]:
        drop_db()

        print "DB deleted!"


    elif args.command == Commands[2] and args.data:
        with open(args.data, 'r') as f:
            seed_data = json.loads(f.read())
        for item_class in seed_data:
            items = seed_data[item_class]
            print items
            for item in items:
                endpoint = os.path.join(API_ENDPOINT_PREFIX, item_class)
                create_sample_db_entry(endpoint, item)

        print "\nSeed data added to database!"


    elif args.command == Commands[3]:
        watch()


    elif args.command == Commands[4]:
        config = {}
        if args.twbs:
            config['twbs'] = args.twbs
        if len(config.keys()) == 0:
            print "Enter keyword argument to specify types to fetch"
        download(**config)


    elif args.command == Commands[5]:
        serve()

    elif args.command == Commands[6]:
        recreate_db()
        print "Deleted and re-created db!"

    elif args.command == Commands[7]:
        create_test_user()
        print "Created test user!"

    else:
        print "Possible commands are " 
        print_cmds()
        raise Exception('Invalid command %s; possibly not enough argument supplied' % args.command)

if __name__ == '__main__':
    main()


