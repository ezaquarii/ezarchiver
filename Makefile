ENVDIR ?= env
DESTDIR ?= ienv

all:
	@echo "EZ Aarchiver makefile - Chris Narkiewicz <hello@ezaquarii.com>"
	@echo
	@echo "Targets:"
	@echo
	@echo " * install DESTDIR=/my/dest/ - installs EZ Archiver"
	@echo " * env                       - make virtual environtment (development)"
	@echo " * distclean                 - cleans up all generated files"
	@echo

$(ENVDIR):
	virtualenv $(ENVDIR)
	ln -s ezarchiver $(ENVDIR)/lib/python2.7/site-packages # so the scripts can invoke python modules
	cp scripts/* $(ENVDIR)/bin/
	$(ENVDIR)/bin/pip install --find-links duplicity -r requirements.txt
	$(ENVDIR)/bin/pip install -r requirements_dev.txt

$(DESTDIR)/bin:
	virtualenv $(DESTDIR)

install: $(ENVDIR) $(DESTDIR)/bin
	$(ENVDIR)/bin/python setup.py bdist_wheel
	$(DESTDIR)/bin/pip install --find-links $(CURDIR)/duplicity $(CURDIR)/dist/ezarchiver-1.0.0-py2-none-any.whl

distclean:
	rm -rf env
	rm -rf ienv
	rm -rf build
	rm -rf dist
	rm -rf ezarchiver.egg-info
	find -type d -name .pytest_cache | xargs rm -rf
