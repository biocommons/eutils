README.html: README.rst
	rst2html <$< >$@


develop:
	python setup.py develop

test:
	python setup.py nosetests


.PHONY: clean cleaner cleanest distclean
clean:
	find . -name \*~ -print0 | xargs -0r rm -f
cleaner: clean
	find . -name \*.pyc -print0 | xargs -0r rm -f
cleanest distclean: cleaner
	rm -fr *.egg *.egg-info
