#!/usr/bin/python
#coding:utf-8

import os
import os.path
import signal
import sys
import getopt
import inspect
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
        iconpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+'/icon.png'
        resticonpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+'/rest.png'
        self.indicator = appindicator.Indicator.new(
            self.app,
            os.path.abspath(iconpath),
            appindicator.IndicatorCategory.OTHER
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("loading...", self.app)
        self.update = Thread(target=self.show_seconds, args=[filename, iconpath, resticonpath])

        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def show_seconds(self, filename, iconpath, resticonpath):
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
                isWorking = 1
            else:
                mention = '休息时间～～～'
                isWorking = 0

            if isWorking == 1:
                GObject.idle_add(
                    self.indicator.set_icon,
                    os.path.abspath(iconpath),
                    priority=GObject.PRIORITY_DEFAULT
                )
                GObject.idle_add(
                    self.indicator.set_label,
                    mention, self.app,
                    priority=GObject.PRIORITY_DEFAULT
                )
            else:
                GObject.idle_add(
                    self.indicator.set_icon,
                    os.path.abspath(resticonpath),
                    priority=GObject.PRIORITY_DEFAULT
                )
                GObject.idle_add(
                    self.indicator.set_label,
                    mention, self.app,
                    priority=GObject.PRIORITY_DEFAULT
                )

            time.sleep(0.2)

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
