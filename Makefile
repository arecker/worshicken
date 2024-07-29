venv/bin/python: requirements/prod.txt
	rm -rf ./venv/
	$(shell which python) -m venv ./venv --copies
	./venv/bin/pip install --upgrade --quiet pip
	./venv/bin/pip install -r requirements/prod.txt --quiet

.PHONY: dev
dev: venv/bin/python
	./venv/bin/pip install -r requirements/dev.txt --quiet

.PHONY: clean
clean:
	rm -rf ./venv/
	rm -rf ./tmp/*
