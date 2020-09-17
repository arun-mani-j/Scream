import sys
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk
from .command_line_options import options
from .model import Model
from .view import View


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        Gtk.Application.__init__(
            self,
            *args,
            application_id="org.scream.scream",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
            **kwargs
        )
        GLib.set_prgname("Scream")
        for option in options:
            self.add_main_option(*option)
        self.model: Model
        self.view: View

        self.filename = None
        self.quick = False

        self.connect("activate", self._activate)
        self.connect("handle-local-options", self._handle_local_options)
        self.connect("startup", self._startup)

    def _activate(self, app):

        window = self.view.window
        window.set_application(self)
        window.present()
        if self.filename:
            self.view.open_session(None, self.filename)
        if self.quick:
            self.view.execute_actions(None)

    def _handle_local_options(self, app, options: GLib.VariantDict):

        args = options.end().unpack()
        if "quick" in args and not args.get("filename", None):
            sys.stderr.write("No file specified but --quick was used.\n")
            sys.stderr.flush()
            return 1
        self.start(**args)
        return -1

    def _startup(self, _):

        self.model = Model()
        self.view = View(self.model)

    def start(self, filename=None, quick=False):

        self.filename = filename
        self.quick = quick
