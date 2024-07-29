actual_python := $(shell python --version)
expected_python := Python $(shell cat .python-version | tr -d '\n')
ifneq ($(actual_python),$(expected_python))
    $(error wanted "$(expected_python)", detected "$(actual_python)")
endif

.PHONY: all
all: lint test squash

venv/bin/python: requirements.txt
	rm -rf ./venv
	python -m venv ./venv --copies
	./venv/bin/pip install --upgrade --quiet pip
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install --quiet --upgrade jedi-language-server isort pyflakes ipython

.PHONY: test
test: venv/bin/python
	./manage.py test

.PHONY: lint
lint: venv/bin/python
	./venv/bin/pip install --quiet --upgrade flake8
	./venv/bin/flake8 --color never --ignore E501 --exclude ./venv/ .

.PHONY: squash
squash: venv/bin/python
	rm -f ./tmp/db.sqlite3
	rm -rf ./db/migrations/*.py
	./manage.py makemigrations db --no-color
	./manage.py migrate --no-color

.PHONY: run
run: squash
	./manage.py loaddata users.json
	./manage.py loaddata instruments.json
	./manage.py changepassword alex@reckerfamily.com
	./manage.py runserver

.PHONY: shell
shell: venv/bin/python
	./manage.py shell

.PHONY: clean
clean:
	rm -f ./tmp/db.sqlite3
	rm -rf ./venv
