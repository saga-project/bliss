To generate the API documentation, run this in the Bliss **root directory**:

    epydoc -v --no-frames --config=docs/epydoc.bliss.saga.cfg

With Sphinx: 

merzky@thinkie:~/saga/bliss (feature/sphinx $) $ make -n
make -C docs html

merzky@thinkie:~/saga/bliss (feature/sphinx $) $ make -C docs html -n
make: Entering directory `/home/merzky/saga/bliss/docs'
sphinx-build -b html -d _build/doctrees   . _build/html
echo
echo "Build finished. The HTML pages are in _build/html."
make: Leaving directory `/home/merzky/saga/bliss/docs'

