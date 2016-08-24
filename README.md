## Stash

Stash gives designers an easy way to browse and share their work.

### Dependencies

  - Python 2.7+
  - Postgres 9.3
  - Unix Env (Mac OSX preferred)
  - VirtualEnv

### Install
If you're cloning for the first time, run "make install" and follow the 
directions to set up the virtual environment. 

### Reference
Test database can be viewed via "sqlite3 /tmp/stash.db", although it's
easier to just use Python console + SqlAlchemy

Refer to Flask documentation for most things. To keep things simple,
we're only using SqlAlchemy's models, nothing too special.

###First time

	chmod a+x ./run.py

	./run.py seed_data --data=<your_data_source>

	./run.py server 

