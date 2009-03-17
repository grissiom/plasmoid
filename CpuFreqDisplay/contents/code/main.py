# Written by Grissiom chaos.proton@gmail.com

# This script is inspired by ruby-cpufreq plasmoid and released under GPL
# license. It noly goal is to display CPU frequency. If you want to do CPU
# scaling, try PowerDevil.

import subprocess as sp

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

		# from plasmaengineexplorer, solidservice seems not working on my box.
		# FIXME: What if the box is signal cored or cores with different frequency?
		f = sp.Popen(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"],
				close_fds = True, stdout = sp.PIPE).stdout
		afreq = f.readlines()[0].split(' ')[:-1]# the last byte is '\n'
		self.afreq = map(int, afreq)
		self.afreq.sort()
		self.cfreq = 0
		self.update_freq()

		self.timer = QTimer(self)
		self.connect(self.timer, SIGNAL('timeout()'), self.update_freq)
		self.timer.start(1000)

	def update_freq(self):
		# FIXME: this may cause buffer overflow, but I don't know how to fix yet...
		f = sp.Popen(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"],
				close_fds = True, stdout = sp.PIPE).stdout
		cfreq = int(f.readlines()[0])
		if self.cfreq != cfreq:
			self.update()
		self.cfreq = cfreq

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

		# TODO:optimization should goes here
		font = p.font()
		ps = font.pixelSize()
		p.setFont(font)
		while p.boundingRect(rect, Qt.AlignTop | Qt.AlignLeft, text).width() < rect.width()\
		      and p.boundingRect(rect, Qt.AlignTop | Qt.AlignLeft, text).height() < rect.height():
			ps += 1
			font.setPixelSize(ps)
		p.setFont(font)

		p.setPen(self.color)
		p.drawText(rect, Qt.AlignTop | Qt.AlignLeft,  text)
		p.restore()

def CreateApplet(p):
	return CpuFreqDisplay(p)
