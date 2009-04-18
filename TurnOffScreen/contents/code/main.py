# Written by Grissiom chaos.proton@gmail.com

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QGraphicsLinearLayout, QWidget

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import KIcon, KGlobalSettings, KShortcutsDialog, KShortcutsEditor, \
                KShortcutWidget

import dbus

#import gui

class TurnOffScreen(plasmascript.Applet):
	def __init__(self, parent, args = None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
                #TODO: have a configuration interface to set keybroad shortcut
		#self.setHasConfigurationInterface(True)
		self.setAspectRatioMode(Plasma.ConstrainedSquare)
                self.setBackgroundHints(self.NoBackground)

                self.sessionBus = dbus.SessionBus()
                self.powerdevil = self.sessionBus.get_object('org.freedesktop.PowerManagement',
                                                             '/modules/powerdevil')

                self.icon= Plasma.IconWidget(KIcon('preferences-desktop-screensaver'), '', self.applet)
                if KGlobalSettings.singleClick():
                        self.connect(self.icon, SIGNAL('clicked()'), self.turn_off_screen)
                else:
                        self.connect(self.icon, SIGNAL('doubleClicked()'), self.turn_off_screen)
                self.connect(self, SIGNAL('active()'), self.turn_off_screen)

                self.layout = QGraphicsLinearLayout(self.applet)
                self.layout.setContentsMargins(0, 0, 0, 0)
                self.layout.setSpacing(0)
                self.layout.addItem(self.icon)
                self.setLayout(self.layout)
                self.resize(25, 25)

        #def showConfigurationInterface(self):
        #        self.con_short = KShortcutWidget(None)
        #        self.con_short.show()

        def turn_off_screen(self):
                self.powerdevil.turnOffScreen(dbus_interface='org.kde.PowerDevil')

def CreateApplet(p):
	return TurnOffScreen(p)
