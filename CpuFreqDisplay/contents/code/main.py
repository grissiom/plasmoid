# Written by Grissiom chaos.proton@gmail.com

# This script is inspired by ruby-cpufreq plasmoid and released under GPL
# license. It noly goal is to display CPU frequency. If you want to do CPU
# scaling, try PowerDevil.

# Thanks to:
# wd <wd@wdicc.com> for sharing his/her script that teach me to use file object.
# Wang Hoi <zealot.hoi@gmail.com> for teaching me getting font from Plasma.font()

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

class CpuFreqDisplay(plasmascript.Applet):
	def __init__(self, parent, args = None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
		self.setHasConfigurationInterface(False)
		self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

		self.ft = self.font()
		self.ft.setPixelSize(30)
		self.width = 0
		self.height = 0

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
		self.resize(150, 25)

		self.startTimer(1000)

	def update_freq(self):
		f = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", 'rb')
		cfreq = int(f.read().strip())
		f.close()
		if self.cfreq != cfreq:
			self.cfreq = cfreq
			if self.cfreq == self.afreq[0]:
				self.color = Qt.green
			elif self.cfreq == self.afreq[-1]:
				self.color = Qt.red
			else:
				self.color = Qt.yellow
			if self.cfreq > 1100000:
				self.text = "%.2fGHz" % (self.cfreq / 1000000.0)
			else:
				self.text = "%dMHz" % (self.cfreq / 1000)
			self.update()

	def timerEvent(self, event):
		self.update_freq()

	def paintInterface(self, p, option, rect):
		p.save()
		if self.width != rect.width() or self.height != rect.height():
			self.update_font(rect.width(), rect.height())
			self.width, self.height = rect.width(), rect.height()
		p.setFont(self.ft)
		p.setPen(self.color)
		p.drawText(rect, Qt.AlignHCenter, self.text)
		p.restore()

	#def constraintsEvent(self, con):
	#        if con & (Plasma.SizeConstraint | Plasma.StartupCompletedConstraint):

	def update_font(self, w, h):
		if self.formFactor() == Plasma.Vertical:
			br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			while br.width() < w:
				self.ft.setPixelSize(self.ft.pixelSize() + 1)
				br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			while br.width() >= w and self.ft.pixelSize() >= 2:
				self.ft.setPixelSize(self.ft.pixelSize() - 1)
				br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			self.setMinimumHeight(br.height() + self.size().height() - h)
			self.setMaximumHeight(br.height() + self.size().height() - h)
			self.setMinimumWidth(self.size().width() - w + 8)
			self.setMaximumWidth(16777215)
		elif self.formFactor() == Plasma.Horizontal:
			br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			while br.height() < h:
				self.ft.setPixelSize(self.ft.pixelSize() + 1)
				br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			while br.height() >= h and self.ft.pixelSize() >= 2:
				self.ft.setPixelSize(self.ft.pixelSize() - 1)
				br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			self.setMinimumWidth(br.width() + self.size().width() - w)
			self.setMaximumWidth(br.width() + self.size().width() - w)
			self.setMinimumHeight(self.size().height() - h + 8)
			self.setMaximumHeight(16777215)
		else:
			self.ft.setPixelSize(h)
			br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			while br.width() < w and br.height() < h:
				self.ft.setPixelSize(self.ft.pixelSize() + 1)
				br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			while self.ft.pixelSize() >= 2 and (br.width() > w or br.height() > h):
				self.ft.setPixelSize(self.ft.pixelSize() - 1)
				br = QFontMetrics(self.ft).boundingRect(QString(self.text))
			self.setMinimumSize(self.size().width() - w + 8, self.size().height() - h + 8)
			self.setMaximumSize(16777215, 16777215)

def CreateApplet(p):
	return CpuFreqDisplay(p)
