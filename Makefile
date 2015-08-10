ENV=./env/bin
PYTHON=$(ENV)/python
PIP=$(ENV)/pip

dev: 
	$(PIP) install -r requirements/dev.txt --upgrade

prod:
	$(PIP) install -r requirements/prod.txt --upgrade

env:
	virtualenv -p `which python3` env

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.egg-info

flake8:
	flake8

lint: flake8

test:
	$(PYTHON) setup.py test

#run:
#	$(ENV)/python gso.py

freeze:
	mkdir -p requirements
	$(PIP) freeze > requirements/dev.txt

