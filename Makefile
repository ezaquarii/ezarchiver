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
	git clean -fdx

dpkg: distclean
	gbp buildpackage

