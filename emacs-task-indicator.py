#!/usr/bin/python
#coding:utf-8

import os
import os.path
import signal
import sys
import getopt
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject
import time
import datetime
from threading import Thread

class Indicator():
    def __init__(self, filename):
        self.app = 'EmacsTaskIndicator'
        iconpath = 'icon.png'
        self.indicator = appindicator.Indicator.new(
            self.app,
            os.path.abspath(iconpath),
            appindicator.IndicatorCategory.OTHER
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("loading...", self.app)
        self.update = Thread(target=self.show_seconds, args=[filename])

        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def show_seconds(self, filename):
        while True:
            if os.path.isfile(filename):
                file = open(os.path.abspath(filename), "r")
                line = file.readline()
                res = line.split()
                start_time = datetime.datetime.fromtimestamp(int(res[0]))
                elapsed = datetime.datetime.now() - start_time
                seconds = elapsed.seconds + elapsed.days * 86400
                h = "%02d" % (seconds / 3600)
                m = "%02d" % (seconds % 3600 / 60)
                mention = '['+h+':'+m+'] '+res[1]
            else:
                mention = '休息时间～～～'
            GObject.idle_add(
                self.indicator.set_label,
                mention, self.app,
                priority=GObject.PRIORITY_DEFAULT
            )
            time.sleep(5)

    def stop(self, source):
        gtk.main_quit()


def check(argv):
    filename = ''

    try:
        opts, args = getopt.getopt(argv, "hf:", ["ifile="])
    except getopt.GetoptError:
        print('emacs-task-indicator.py -f <filename>')
        sys.exit(2)

    if len(opts) != 1:
        print('emacs-task-indicator.py -f <filename>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('emacs-task-indicator.py -f <filename>')
            sys.exit()
        elif opt in ("-f", "--ifile"):
            filename = arg

    return filename



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    inputfile = ''
    inputfile = check(sys.argv[1:])
    Indicator(inputfile)
    GObject.threads_init()
    gtk.main()
