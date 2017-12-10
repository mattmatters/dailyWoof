init:
	pip install --no-cache-dir -r requirements.txt
	python -m textblob.download_corpora
	python setup.py install
test:
	pytest tests
.PHONY: init test
