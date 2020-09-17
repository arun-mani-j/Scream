from gi.repository import GdkX11
from gi.repository import Wnck


class Server:
    def __init__(self):

        self.display = GdkX11.X11Display.get_default()
        self.screen = Wnck.Screen.get_default()
        self.screen.force_update()
        self.connect = self.screen.connect

    def get_windows(self, name=""):

        for window in self.screen.get_windows():
            if name in window.get_name():
                yield window

    def get_X11windows(self, name=""):

        for window in self.screen.get_windows():
            if name in window.get_name():
                xid = window.get_xid()
                yield GdkX11.X11Window.lookup_for_display(self.display, xid)
