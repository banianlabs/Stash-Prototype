from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.url_map.strict_slashes = False
	
# Initialize submodules
import stash.core
import stash.models
import stash.routes
