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
	rm -f distribute-*
cleanest distclean: cleaner
	find . -name \*.pyc -print0 | xargs -0r rm -f
	rm -fr eutils.egg-info
