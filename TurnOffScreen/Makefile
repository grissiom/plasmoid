.PHONY:all install uninstall reinstall view tarball

PRONAME=TurnOffScreen

all: install
tarball: $(PRONAME).zip

install: ${PRONAME}.zip
	plasmapkg -i ${PRONAME}.zip

uninstall:
	plasmapkg -r ${PRONAME}

reinstall: uninstall install

$(PRONAME).zip: metadata.desktop contents/code/main.py
	zip -r ${PRONAME}.zip . -x *~ contents/code/*~ .* ${PRONAME}.zip

view:
	plasmoidviewer ${PRONAME}
