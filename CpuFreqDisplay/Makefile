.PHONY:all install uninstall reinstall view

PRONAME=CpuFreqDisplay

all: install

install: ${PRONAME}.zip
	plasmapkg -i ${PRONAME}.zip

uninstall:
	plasmapkg -r ${PRONAME}

reinstall: uninstall install

CpuFreqDisplay.zip: metadata.desktop contents/code/main.py
	zip -r ${PRONAME}.zip . -x *~ contents/code/main.py~ .* ${PRONAME}.zip

view:
	plasmoidviewer ${PRONAME}
