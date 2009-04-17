.PHONY:all install uninstall reinstall view tarball

PRONAME=TurnOffScreen

all: install
tarball: $(PRONAME).zip

install: ${PRONAME}.zip
	plasmapkg -i ${PRONAME}.zip

uninstall:
	plasmapkg -r ${PRONAME}

reinstall: uninstall install

$(PRONAME).zip: metadata.desktop contents/code/main.py contents/code/gui.py
	zip -r ${PRONAME}.zip . -x *~ contents/code/*~ .* ${PRONAME}.zip

contents/code/gui.py: contents/code/gui.qrc
	pyrcc4 $^ > $@

view:
	plasmoidviewer ${PRONAME}
