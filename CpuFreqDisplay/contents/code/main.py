# Written by Grissiom chaos.proton@gmail.com

# This script is inspired by ruby-cpufreq plasmoid and released under GPL
# license. It noly goal is to display CPU frequency. If you want to do CPU
# scaling, try PowerDevil.

# Thanks to:
# wd <wd@wdicc.com> for sharing his/her script that teach me to use file object.
# Wang Hoi <zealot.hoi@gmail.com> for teaching me getting font from Plasma.font()

from PyQt4.QtCore import QTimer, Qt, SIGNAL
#from PyQt4.QtGui import QFont

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

class CpuFreqDisplay(plasmascript.Applet):
	def __init__(self, parent, args = None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
		self.setHasConfigurationInterface(False)
		self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

		self.ft = self.font()
		# set to a reasonable pixelSize here so we have less loop
		# later.
		self.ft.setPixelSize(30)

		# from plasmaengineexplorer, solidservice seems not working on
		# my box. So I cannot use DataEngin here...
		# signal cored machine will have /sys/devices/system/cpu/cpu0/ too.
		# FIXME: What if the box have cores with different frequency?
		f = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies", 'rb')
		afreq = f.read().strip().split(' ')
		f.close()
		self.afreq = map(int, afreq)
		self.afreq.sort()
		self.cfreq = 0
		self.update_freq()

		self.startTimer(1000)

	def update_freq(self):
		f = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", 'rb')
		cfreq = int(f.read().strip())
		f.close()
		if self.cfreq != cfreq:
			self.cfreq = cfreq
			self.update()

	def timerEvent(self, event):
		self.update_freq()

	def paintInterface(self, p, option, rect):
		p.save()
		if self.cfreq == self.afreq[0]:
			self.color = Qt.green
		elif self.cfreq == self.afreq[-1]:
			self.color = Qt.red
		else:
			self.color = Qt.yellow
		if self.cfreq > 1000000:
			text = "%.2fGHz" % (self.cfreq / 1000000.0)
		else:
			text = "%.2fMHz" % (self.cfreq / 1000.0)

		# TODO: need optimization
		ps = self.ft.pixelSize()
		p.setFont(self.ft)
		while p.boundingRect(rect, Qt.AlignTop | Qt.AlignLeft, text).width() < rect.width() and\
		      p.boundingRect(rect, Qt.AlignTop | Qt.AlignLeft, text).height() < rect.height():
			ps += 1
			self.ft.setPixelSize(ps)
			p.setFont(self.ft)
		while p.boundingRect(rect, Qt.AlignTop | Qt.AlignLeft, text).width() > rect.width() or\
		      p.boundingRect(rect, Qt.AlignTop | Qt.AlignLeft, text).height() > rect.height():
			ps -= 1
			self.ft.setPixelSize(ps)
			p.setFont(self.ft)

		p.setPen(self.color)
		p.drawText(rect, Qt.AlignTop | Qt.AlignLeft,  text)
		p.restore()

def CreateApplet(p):
	return CpuFreqDisplay(p)
