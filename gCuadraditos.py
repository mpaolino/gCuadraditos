# -*- coding: utf-8 -*-

#from gi.repository import Gtk
import pygtk
pygtk.require("2.0")
import gtk
import pygst
pygst.require("0.10")
import gst
import logging
import aplay
from constants import sound_click
import urlparse

logger = logging.getLogger('gCuadraditos:cuadraditos.py')


gst.debug_set_active(True)
gst.debug_set_colored(False)

if logging.getLogger().level <= logging.DEBUG:
    gst.debug_set_default_threshold(gst.LEVEL_WARNING)
else:
    gst.debug_set_default_threshold(gst.LEVEL_ERROR)


class gCuadraditos:

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
     
    def __init__(self):
    
        builder = gtk.Builder()
        builder.add_from_file("ui.xml") 
        
        self.window = builder.get_object("window1")
        self.button = builder.get_object("detectar")
        self.button.connect("clicked", self.start_stop)
        self.capture_window = builder.get_object("drawingarea")
        builder.connect_signals(self)       

        self.VIDEO_WIDTH = 352
        self.VIDEO_HEIGHT = 288
        self.VIDEO_FRAMERATE = 5
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
            return
        if message.structure.get_name() == 'prepare-xwindow-id':
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self.capture_window.window.xid)
                                    
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

    def _clipboard_get_func_cb(self, clipboard, selection_data, info, data):
        selection_data.set("text/uri-list", 8, data)

    def _clipboard_clear_func_cb(self, clipboard, data):
        pass

    def _copy_URI_to_clipboard(self):
        gtk.Clipboard().set_with_data([('text/uri-list', 0, 0)],
                                      self._clipboard_get_func_cb,
                                      self._clipboard_clear_func_cb,
                                      self.last_detection)
        return True

    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.playing = True

    def pause(self):
        self.pipeline.set_state(gst.STATE_PAUSED)
        self.playing = False

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)
        self.playing = False

    def start_stop(self, w):
        if self.button.get_label() == "Detectar":
            self.button.set_label("Detener")
            self.play()
        else:
            self.stop()
            self.button.set_label("Detectar")

    def _on_message_cb(self, bus, message):
        t = message.type
        #if t == gst.MESSAGE_EOS:
        #   if self._eos_cb:
        #        cb = self._eos_cb
        #        self._eos_cb = None
        #        cb()
        if t == gst.MESSAGE_ELEMENT:
            s = message.structure
            if s.has_name("barcode"):
                self.stop()
                self.window.hide()
                aplay.play(sound_click)
                self.last_detection = s['symbol']
                parsedurl = urlparse.urlparse(s['symbol'])
                if parsedurl.scheme in self.recognized_schemes:
                    #alert = TimeoutAlert(60)
                    #alert.remove_button(gtk.RESPONSE_CANCEL)
                    #alert.props.title = 'Direccion detectada!'
                    #alert.props.msg = 'La dirección fue copiada al ' +\
                    #                  'portatapeles. Acceda al ' +\
                    #                  'marco de Sugar y haga click sobre ' +\
                    #                  'ella para abrirla en el navegador.'
                    #alert.connect('response', self._alert_uri_response_cb)
                    #self.ca.add_alert(alert)
                    self._copy_URI_to_clipboard()
                    #self.ca.alert.show()
                else:
                    #alert = ConfirmationAlert()
                    #alert.props.title = 'Texto detectado. ' +\
                    #                    '¿Desea copiarlo al portapapeles?'
                    #alert.props.msg = s['symbol']
                    #alert.connect('response', self._alert_text_response_cb)
                    #self.ca.add_alert(alert)
                    #self.ca.alert.show()
                    pass

        elif t == gst.MESSAGE_ERROR:
            #todo: if we come out of suspend/resume with errors, then get us
            #      back up and running...
            #todo: handle "No space left on the resource.gstfilesink.c"
            #err, debug = message.parse_error()
            pass


if __name__ == "__main__":
    cuadraditos = gCuadraditos()
    cuadraditos.window.show()
    gtk.main()
