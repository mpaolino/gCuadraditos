# -*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk

import pygst
pygst.require("0.10")
import gst
import logging
import aplay
from constants import (sound_click, icon_file, ui_file)
import urlparse
import gobject

logger = logging.getLogger('gCuadraditos:cuadraditos.py')


gst.debug_set_active(True)
gst.debug_set_colored(False)

if logging.getLogger().level <= logging.DEBUG:
    gst.debug_set_default_threshold(gst.LEVEL_WARNING)
else:
    gst.debug_set_default_threshold(gst.LEVEL_ERROR)


class gCuadraditos:

    def on_window_destroy(self, widget, data=None):
        self.stop()
        gtk.main_quit()
     
    def __init__(self):
    
        builder = gtk.Builder()
        builder.add_from_file(ui_file) 
        
        self.window = builder.get_object("window1")
        self.window.set_icon_from_file(icon_file)
        
        self.button = builder.get_object("detectar")
        self.button.connect("clicked", self.start_stop)
        self.link_button = builder.get_object("linkbutton")
        self.link_button.set_sensitive(False)
        self.capture_window = builder.get_object("drawingarea")
        builder.connect_signals(self)       
        self.window.show_all()

        self.VIDEO_WIDTH = 352
        self.VIDEO_HEIGHT = 288
        self.recognized_schemes = ['file', 'ftp', 'gopher', 'http', 'https',
                                   'imap', 'mailto', 'mms', 'news', 'nntp',
                                   'prospero', 'rsync', 'rtsp', 'rtspu',
                                   'sftp', 'shttp', 'sip', 'sips', 'snews',
                                   'svn', 'svn+ssh', 'telnet', 'wais']

        self.pipeline = gst.Pipeline("my-pipeline")
        self.create_pipeline()

        bus = self.pipeline.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        self.SYNC_ID = bus.connect('sync-message::element',\
                                   self._on_sync_message_cb)
        self.MESSAGE_ID = bus.connect('message', self._on_message_cb)

    def _on_sync_message_cb(self, bus, message):
        if message.structure is None:
            return False
        if message.structure.get_name() == 'prepare-xwindow-id':
            gtk.gdk.threads_enter()
            gtk.gdk.display_get_default().sync()
            win_id = self.capture_window.window.xid
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(win_id)
            gtk.gdk.flush()
            gtk.gdk.threads_leave()
            
    def create_pipeline(self):
        src = gst.element_factory_make("v4l2src", "camsrc")
        srccaps = gst.Caps('video/x-raw-yuv, width=%s, height=%s' %\
                           (self.VIDEO_WIDTH, self.VIDEO_HEIGHT))
        zbar = gst.element_factory_make("zbar")

        self.pipeline.add(src, zbar)
        src.link(zbar, srccaps)

        xvsink = gst.element_factory_make("xvimagesink", "xvsink")
        xv_available = xvsink.set_state(gst.STATE_PAUSED) != \
                       gst.STATE_CHANGE_FAILURE
        xvsink.set_state(gst.STATE_NULL)

        if not xv_available:
            self.__class__.log.error('xv not available cannot capture video')
            return

        xvsink.set_property("sync", False)
        self.pipeline.add(xvsink)
        zbar.link(xvsink)


    def _set_link_button(self, uri):
        self.link_button.set_uri(uri)
        self.link_button.set_label(uri)
        self.link_button.set_sensitive(True)

    def play(self):
        self.button.set_label("Detener")
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.capture_window.show()
        self.playing = True

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)
        self.playing = False
        self.capture_window.hide()
        self.button.set_label("Detectar")

    def start_stop(self, w):
        if self.button.get_label() == "Detectar":
            self.play()
        else:
            self.stop()

    def _on_message_cb(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_ELEMENT:
            s = message.structure
            if s.has_name("barcode"):
                self.stop()
                aplay.play(sound_click)
                self.last_detection = s['symbol']
                parsedurl = urlparse.urlparse(s['symbol'])
                if parsedurl.scheme in self.recognized_schemes:
                    self._set_link_button(s['symbol'].encode('utf-8'))
                else:
                    gtk.gdk.threads_enter()
                    the_dialog = gtk.MessageDialog(
                                                self.window,
                                                gtk.DIALOG_MODAL,
                                                type=gtk.MESSAGE_INFO,
                                                buttons=gtk.BUTTONS_OK)
                    the_dialog.set_markup("<b>%s</b>" % 'Texto detectado:')
                    the_dialog.format_secondary_markup(s['symbol'].\
                                                        encode('utf-8'))
                    the_dialog.run()
                    the_dialog.destroy()
                    gtk.gdk.threads_leave()
                    
        elif t == gst.MESSAGE_ERROR:
            #todo: if we come out of suspend/resume with errors, then get us
            #      back up and running...
            #todo: handle "No space left on the resource.gstfilesink.c"
            #err, debug = message.parse_error()
            pass


if __name__ == "__main__":
    cuadraditos = gCuadraditos()
    gtk.gdk.threads_init()
    gobject.idle_add(cuadraditos.play)
    gtk.main()
