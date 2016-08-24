install:
	@echo "Set up virtual environment"
	virtualenv venv
	@echo "Now, run source venv/bin/activate. Then run make install2"

install2:
	@echo "Install necessary requirements"
	npm install -g less
	pip install -r requirements.txt
	@mkdir stash/static/css
	@echo "Done."	

	@echo
	@echo "First, ./run create_db && ./run seed_db --seedfile data/db_items.json"
	@echo "Then, ./run server to run the server"

server:
	@./run.py server

test:
	@python -m stash.tests.api_test
