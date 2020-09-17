from gi.repository import Atspi
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GLib
from gi.repository import Wnck


class Model:
    def __init__(self):

        self.display = GdkX11.X11Display.get_default()
        self.screen = Wnck.Screen.get_default()
        self.props = {
            "window": None,
            "fmt": "jpg",
            "x1": None,
            "y1": None,
            "x2": None,
            "y2": None,
        }
        Atspi.init()

    def capture(
        self,
        window: GdkX11.X11Window,
        filename: str,
        type: str,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ):

        pixbuf = self.get_pixbuf_x(window, x1, y1, x2, y2)
        pixbuf.savev(filename, type, [], [])

    def connect(self, signal, callback, *args, **kwargs):
        def forwarder(scr, win=None):
            if win:
                callback(win, *args, **kwargs)
            else:
                callback(scr, *args, **kwargs)

        self.screen.connect(signal, forwarder)

    def execute(self, filename: str, keyval: int):

        if keyval:
            Atspi.generate_keyboard_event(keyval, None, Atspi.KeySynthType.PRESSRELEASE)
        self.capture(
            filename=filename,
            window=self.props["window"],
            type=self.props["type"],
            x1=self.props["x1"],
            y1=self.props["y1"],
            x2=self.props["x2"],
            y2=self.props["y2"],
        )

    def get_pixbuf_wnck(self, window: Wnck.Window, x1: int, y1: int, x2: int, y2: int):

        x_window = self.wnck_to_x(window)
        return self.get_pixbuf_x(x_window, x1, y1, x2, y2)

    def get_pixbuf_x(self, window: GdkX11.X11Window, x1, y1, x2, y2):

        pixbuf = Gdk.pixbuf_get_from_window(window, x1, y1, x2, y2)
        assert pixbuf is not None
        return pixbuf

    def get_windows_wnck(self, name=""):

        for window in self.screen.get_windows():
            if name in window.get_name():
                yield window

    def get_windows_x(self, name=""):

        for window in self.screen.get_windows():
            if name in window.get_name():
                yield window

    def wnck_to_x(self, window: Wnck.Window) -> GdkX11.X11Window:

        xid = window.get_xid()
        x_window = GdkX11.X11Window.foreign_new_for_display(self.display, xid)
        return x_window
