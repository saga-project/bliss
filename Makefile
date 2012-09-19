

SPHINXBUILD   = sphinx-build -a -E -n -c docs/
BUILDDIR      = docs/


.PHONY: docs clean install install_clean test all

all: docs

docs:
	$(SPHINXBUILD) -b html . $(BUILDDIR)/html

clean:
	@rm -rf $(BUILDDIR)/html
	@find . -name \*.pyc -exec rm {} \;
	@find . -name \*.bak -exec rm {} \;
	@rm -rf docs/html/

install:
	@sudo python ./setup.py install

install_clean:
	@sudo rm -rf bliss.egg-info/
	@sudo rm -rf build/
	@sudo rm -rf /usr/local/lib/python*/dist-packages/bliss*

test:
	python -c "import bliss.saga as saga" 

