
all: uninstall zipfile
	plasmapkg -i ../CpuFreqDisplay.zip

uninstall:
	plasmapkg -r CpuFreqDisplay

zipfile:metadata.desktop contents/code/main.py
	zip -r ../CpuFreqDisplay.zip . -x *~ contents/code/main.py~ .*
