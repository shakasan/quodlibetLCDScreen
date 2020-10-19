"""
quodlibetLCDScreen
    author : Francois B. (Makotosan/Shakasan)
    licence : GPLv3
    website : https://makotonoblog.be/
"""

import os
import sys

if os.name == "nt" or sys.platform == "darwin":
    from quodlibet.plugins import PluginNotSupportedError
    raise PluginNotSupportedError

from gi.repository import Gtk
from quodlibet.plugins.events import EventPlugin
from quodlibet.qltk import Frame, Icons
from lcd2usb import LCD
import getpass


class MyPlugin(EventPlugin):
    PLUGIN_ID = "quodlibetlcdscreen"
    PLUGIN_NAME = "quodlibetLCDScreen"
    PLUGIN_DESC = "Display Artist/Title on external usb screen"
    PLUGIN_ICON = Icons.PREFERENCES_SYSTEM

    def __init__(self):
        self.lcd = LCD()
        self.lcd.clear()

    def enabled(self):
        self.current = 'Hello'
        self.current2 = getpass.getuser()
        self.lcd.clear()
        self.lcd.write(self.current, 0, 0)
        self.lcd.write(self.current2, 0, 1)

    def disabled(self):
        self.current = 'Bye'
        self.current2 = getpass.getuser()
        self.lcd.clear()
        self.lcd.write(self.current, 0, 0)
        self.lcd.write(self.current2, 0, 1)

    def plugin_on_song_started(self, song):
        if song:
            self.current = str(song['artist'])
            self.current2 = str(song['title'])
        else:
            self.current = ''
            self.current2 = ''
        self.lcd.clear()
        self.lcd.write(self.current.encode("ascii", "ignore"), 0, 0)
        self.lcd.write(self.current2.encode("ascii", "ignore"), 0, 1)

    def PluginPreferences(self, parent):
        def labelTitle(title):
            lbl = Gtk.Label(xalign=1, yalign=0, wrap=True, justify=Gtk.Justification.RIGHT, selectable=True)
            lbl.set_text(title)
            return lbl

        def labelValue(value):
            lbl = Gtk.Label(wrap=True, xalign=0, yalign=0, width_chars=25, selectable=True)
            lbl.set_text(value)
            return lbl

        def labelMarkup(value):
            lbl = Gtk.Label(wrap=True, xalign=0, yalign=0, width_chars=25, selectable=True)
            lbl.set_markup(value)
            return lbl

        vbox = Gtk.VBox(spacing=10)
        stack = Gtk.Stack()

        # setting tab
        gridSettings = Gtk.Grid(column_spacing=12, row_spacing=6)
        gridSettings.insert_row(0)
        # Plugin version
        lbl_lcb_version = labelTitle('USB LCD version : ')
        lblval_lcd_version = labelValue('%s.%s' % self.lcd.version)
        gridSettings.attach(lbl_lcb_version, 0, 0, 1, 1)
        gridSettings.attach(lblval_lcd_version, 1, 0, 1, 1)

        stack.add_titled(gridSettings, 'labelSettings', 'Settings')

        # about tab
        gridAbout = Gtk.Grid(column_spacing=12, row_spacing=6)
        gridAbout.insert_row(0)
        # Plugin version
        lbl_plugin_version = labelTitle('Version : ')
        lblval_plugin_version = labelValue('0.1')
        gridAbout.attach(lbl_plugin_version, 0, 0, 1, 1)
        gridAbout.attach(lblval_plugin_version, 1, 0, 1, 1)
        # Plugin licence
        lbl_plugin_licence = labelTitle('Licence : ')
        lblval_plugin_licence = labelValue('GPL-3.0')
        gridAbout.attach(lbl_plugin_licence, 0, 1, 1, 1)
        gridAbout.attach(lblval_plugin_licence, 1, 1, 1, 1)
        # Plugin author
        lbl_plugin_author = labelTitle('Author : ')
        lblval_plugin_author = labelValue('Francois B (Makoto)')
        gridAbout.attach(lbl_plugin_author, 0, 2, 1, 1)
        gridAbout.attach(lblval_plugin_author, 1, 2, 1, 1)
        # Plugin website
        lbl_plugin_website = labelTitle('Website : ')
        lblval_plugin_website = labelMarkup('<a href="https://makotonoblog.be/quodlibetLCDScreen">https://makotonoblog.be/quodlibetLCDScreen</a>')
        gridAbout.attach(lbl_plugin_website, 0, 3, 1, 1)
        gridAbout.attach(lblval_plugin_website, 1, 3, 1, 1)
        # Plugin repository
        lbl_plugin_gitrepo = labelTitle('Github repo : ')
        lblval_plugin_gitrepo = labelMarkup('<a href="https://github.com/shakasan/quodlibetLCDScreen">https://github.com/shakasan/quodlibetLCDScreen</a>')
        gridAbout.attach(lbl_plugin_gitrepo, 0, 4, 1, 1)
        gridAbout.attach(lblval_plugin_gitrepo, 1, 4, 1, 1)
        stack.add_titled(gridAbout, 'labelAbout', 'About this plugin')

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

        return vbox
