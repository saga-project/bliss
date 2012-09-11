
all: doc

doc:
	@make -C docs
	# @epydoc -v --no-frames --config=docs/epydoc.bliss.saga.cfg

clean:
	@find . -name *.pyc -exec rm  {} \;
	@rm -rf docs/bliss.saga/
	@rm -rf docs/_build/

install_clean:
	@sudo rm -rf bliss.egg-info/
	@sudo rm -rf build/
	@sudo rm -rf /usr/local/lib/python*/dist-packages/bliss*

install:
	@sudo python ./setup.py install

.PHONY: test
test:
	@echo python -c "import bliss.saga as saga" 
	@python -c "import bliss.saga as saga" 

