.PHONY:all install uninstall reinstall view tarball

PRONAME=CpuFreqDisplay

all: install
reinstall: uninstall install
tarball: $(PRONAME).zip

install: ${PRONAME}.zip
	plasmapkg -i ${PRONAME}.zip

uninstall:
	plasmapkg -r ${PRONAME}


$(PRONAME).zip: metadata.desktop contents/code/main.py
	zip -r ${PRONAME}.zip . -x *~ contents/code/main.py~ .* ${PRONAME}.zip

view:
	plasmoidviewer ${PRONAME}
