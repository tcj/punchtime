APPNAME  = punchtime
VERSION  = $(shell git describe --always --match 'v[0-9]*' \
		| sed -e 's/^v//' -e 's,-,.,g')
TARNAME  = $(APPNAME)-$(VERSION)

SPECIN = punchtime.spec.in
SPECFILE = $(SPECIN:.in=)

default: srpm

.PHONY: tar
tar: dist/$(TARNAME).tar.gz

.PHONY: srpm
srpm: tar
	@rpmbuild -ts dist/$(TARNAME).tar.gz

.PHONY: rpm
rpm: tar
	@rpmbuild -tb dist/$(TARNAME).tar.gz

dist/$(TARNAME).tar.gz: $(SPECFILE)
	@echo "Creating dist/$(TARNAME).tar.gz"
	@mkdir -p dist/$(TARNAME)
	@echo "$(VERSION)" > dist/$(TARNAME)/VERSION
	@rm -f dist/$(TARNAME).tar.gz
	@git archive --format=tar --prefix=$(TARNAME)/ \
		HEAD > dist/$(TARNAME).tar
	@tar -C dist --owner=root --group=root -r -f dist/$(TARNAME).tar \
		$(TARNAME)/
	@gzip -f -9 dist/$(TARNAME).tar
	@rm -rf dist/$(TARNAME)

$(SPECFILE): $(SPECIN)
	@mkdir -p dist/$(TARNAME)
	@sed -e "s/@@VERSION@@/$(VERSION)/g" \
		< $(SPECIN) > dist/$(TARNAME)/$(SPECFILE)

.PHONY: clean
clean:
	@rm -rf dist

