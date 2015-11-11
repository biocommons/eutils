# Python project Makefile

.SUFFIXES :
.PRECIOUS :
.PHONY : FORCE
.DELETE_ON_ERROR:

SHELL:=/bin/bash -o pipefail
SELF:=$(firstword $(MAKEFILE_LIST))


############################################################################
#= BASIC USAGE
default: help

#=> help -- display this help message
help: config
	@sbin/extract-makefile-documentation "${SELF}"


############################################################################
#= SETUP, INSTALLATION, PACKAGING

#=> setup
setup: develop

#=> docs -- make sphinx docs
.PHONY: docs
docs: setup build_sphinx

#=> build_sphinx
# sphinx docs needs to be able to import packages
build_sphinx: develop

#=> develop, bdist, bdist_egg, sdist, etc
develop:
	pip install -r etc/dev.reqs
	python setup.py $@

bdist bdist_egg build build_sphinx install sdist: %:
	python setup.py $@

#=> upload
upload: upload_pypi

#=> upload_*: upload to named pypi service (requires config in ~/.pypirc)
upload_%:
	python setup.py bdist_egg bdist_wheel sdist upload -r $*



############################################################################
#= TESTING
# see test configuration in setup.cfg

test-setup: develop

#=> test-with-coverage -- per-commit test target for CI
# see test configuration in setup.cfg
test-with-coverage:
	python setup.py nosetests

#=> test == tox -- use tox for testing
test tox:
	tox

#=> ci-test -- per-commit test target for CI
ci-test: test

#=> ci-test-ve -- test in virtualenv
ci-test-ve: ve
	source ve/bin/activate; \
	make ci-test




############################################################################
#= CLEANUP
.PHONY: clean cleaner cleanest pristine
#=> clean: clean up editor backups, etc.
clean:
	find . -name \*~ -print0 | xargs -0r /bin/rm
#=> cleaner: above, and remove generated files
cleaner: clean
	find . -name \*.pyc -print0 | xargs -0r /bin/rm -f
	/bin/rm -fr build bdist cover dist sdist ve virtualenv*
	-make -C doc clean
#=> cleanest: above, and remove the virtualenv, .orig, and .bak files
cleanest: cleaner
	find . \( -name \*.orig -o -name \*.bak \) -print0 | xargs -0r /bin/rm -v
	/bin/rm -fr *.egg-info .tox .eggs .coverage
#=> pristine: above, and delete anything unknown to mercurial
pristine: cleanest
	hg st -un0 | xargs -0r echo /bin/rm -fv


## <LICENSE>
## Copyright 2014 eutils Contributors (https://bitbucket.org/biocommons/eutils)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
