import json
from typing import Callable, Dict
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Gtk
from gi.repository import GdkX11
from gi.repository import Wnck
from .functions import find_keyval, get_coordinates, infobar_wrapper
from .model import Model
from .runner import Runner


class View:
    def __init__(self, model: Model):

        self.get: Callable[str, Gtk.Widget]
        self.model: Model = model
        self.window: Gtk.Window
        self.windows: Dict[str, Wnck.Window] = {}
        self._init()

    def _init(self):

        builder = Gtk.Builder()
        builder.add_from_file("data/scream.ui")
        builder.connect_signals(self)

        provider = Gtk.CssProvider()
        provider.load_from_path("data/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        infobar = builder.get_object("infobar")

        actions = builder.get_object("actions-store")
        actions_tv = builder.get_object("actions-treeview")

        def text_edited(widget, path, text, i):
            text = text.strip()
            try:
                text = int(text)
                assert text >= 0
            except (AssertionError, ValueError):
                pass
            else:
                actions[path][i] = text

        for i, name in enumerate(("Keyval", "Repeat", "Delay")):
            renderer = Gtk.CellRendererText(editable=True, placeholder_text=name)
            renderer.connect("edited", text_edited, i)
            column = Gtk.TreeViewColumn(name, renderer, text=i)
            actions_tv.append_column(column)

        self.model.connect("window-opened", self.add_window)
        self.model.connect("window-closed", self.remove_window)

        self.get = builder.get_object
        self.window = builder.get_object("window")

    def add_action(self, button: Gtk.Button):

        actions = self.get("actions-store")
        actions.append([0, 1, 2])

    def add_window(self, window: Wnck.Window):

        combobox = self.get("windows-combobox")
        name = window.get_name()
        combobox.append_text(name)
        self.windows[name] = window

    def check_values(self):

        session = self.get_session()

        try:
            wnck_win = self.windows[session["name"]]
        except KeyError:
            raise ValueError("Please choose the window")
        else:
            session["wnck_window"] = wnck_win
            session["x_window"] = self.model.wnck_to_x(wnck_win)

        coords = {"x1": "From x", "y1": "From y", "x2": "To x", "y2": "To y"}
        for arg, name in coords.items():
            val = session[arg]
            if not val:
                raise ValueError(f"<i>{name}</i> is required and should be an integer")

        actions_lx = []
        for i, row in enumerate(session["actions"]):
            keyval, repeat, delay = row
            parsed_row = ([keyval, delay],) * repeat
            actions_lx.extend(parsed_row)
        if not actions_lx:
            raise ValueError("Please add at least one action")
        session["actions"] = actions_lx

        filename = session["destination"]
        if not filename:
            raise ValueError("Choose a directory to save the pictures")

        return session

    def check_position(self, entry: Gtk.Entry):

        pos = entry.get_text().strip()
        if pos:
            try:
                val = int(float(pos))
                assert val >= 0
            except (AssertionError, ValueError):
                entry.set_icon_from_icon_name(
                    Gtk.EntryIconPosition.SECONDARY, "error-app-symbolic"
                )
                entry.set_icon_tooltip_text(
                    Gtk.EntryIconPosition.SECONDARY,
                    "Value should be a positive integer",
                )
            else:
                entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
        else:
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)

    def close_infobar(self, infobar: Gtk.InfoBar, response=None):

        infobar.set_revealed(False)

    @infobar_wrapper
    def execute_actions(self, button: Gtk.Button):

        infobar = self.get("infobar")
        label = self.get("message")
        props = self.check_values()
        actions = props.pop("actions")
        wnck_window = props.pop("wnck_window")
        x_window = props.pop("x_window")
        type = props["type"]
        dest = props.pop("destination")
        args_lx = [
            ((f"{dest}/{i}.{type}", keyval), delay)
            for i, (keyval, delay) in enumerate(actions)
        ]

        abs_x, abs_y = x_window.get_position()
        self.model.props["x1"] = abs(abs_x - props["x1"])
        self.model.props["y1"] = abs(abs_y - props["y1"])

        self.model.props["x2"] = props["x2"]
        self.model.props["y2"] = props["y2"]
        self.model.props["type"] = props["type"]
        self.model.props["window"] = x_window

        self.window.deiconify()
        wnck_window.activate(0)
        runner = Runner(self.model.execute, args_lx)
        runner.start()
        if props["exit"]:
            self.window.close()
        else:
            self.window.present()
            label.set_text(f"Images successfully saved in {dest}")
            infobar.set_message_type(Gtk.MessageType.INFO)
            infobar.set_revealed(True)

    def find_keyval(self, button: Gtk.Button):

        find_keyval()

    def get_session(self):

        combobox = self.get("windows-combobox")
        from_x = self.get("from-x")
        from_y = self.get("from-y")
        to_x = self.get("to-x")
        to_y = self.get("to-y")
        actions = self.get("actions-store")
        direc = self.get("directory-chooser")
        img_type = self.get("image-types")
        exit_ = self.get("exit-check")

        session = {
            "name": combobox.get_active_text(),
            "actions": [list(row) for row in actions],
            "destination": direc.get_filename(),
            "type": img_type.get_active_text(),
            "exit": exit_.get_active(),
        }

        for ent, key in [(from_x, "x1"), (from_y, "y1"), (to_x, "x2"), (to_y, "y2")]:
            try:
                val = int(float(ent.get_text().strip()))
                assert val >= 0
            except (AssertionError, ValueError):
                session[key] = None
            else:
                session[key] = val

        return session

    @infobar_wrapper
    def open_session(self, button: Gtk.Button, filename=None):

        if not filename:
            infobar = self.get("infobar")
            label = self.get("message")

            dialog = Gtk.FileChooserDialog(
                title="Open", parent=self.window, action=Gtk.FileChooserAction.OPEN
            )
            dialog.add_buttons(
                "Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK
            )
            dialog.run()
            dialog.hide()
            filename = dialog.get_filename()

        if not filename:
            return

        try:
            fp = open(filename)
            session = json.load(fp)
        except Exception as e:
            print("Error :", e)
            raise ValueError("Unable to open the session")

        self.set_session(session)

        label.set_text(f"Successfully loaded {filename}")
        infobar.set_message_type(Gtk.MessageType.INFO)
        infobar.set_revealed(True)

    def pick_from(self, button: Gtk.Button):

        from_x = self.get("from-x")
        from_y = self.get("from-y")
        self.window.iconify()
        x, y = get_coordinates()
        self.window.present()

        if not (x and y):
            return
        from_x.set_text(str(x))
        from_y.set_text(str(y))

    def pick_to(self, button: Gtk.Button):

        to_x = self.get("to-x")
        to_y = self.get("to-y")
        self.window.iconify()
        x, y = get_coordinates()
        self.window.present()

        if not (x and y):
            return
        to_x.set_text(str(x))
        to_y.set_text(str(y))

    def refresh_windows(self, button: Gtk.Button):

        combobox = self.get("windows-combobox")
        windows = self.model.get_windows_wnck()

        combobox.remove_all()
        self.windows.clear()

        for window in windows:
            name = window.get_name()
            combobox.append_text(name)
            self.windows[name] = window

    def remove_action(self, button: Gtk.Button):

        actions_tv = self.get("actions-treeview")
        selected = actions_tv.get_selection()
        model, iter_ = selected.get_selected()
        if not iter_:
            return
        model.remove(iter_)

    def remove_window(self, window: Wnck.Window):

        combobox = self.get("windows-combobox")
        ix = list(self.windows.values()).index(window)
        combobox.remove(ix)

    @infobar_wrapper
    def save_session(self, button: Gtk.Button):

        infobar = self.get("infobar")
        label = self.get("message")

        dialog = Gtk.FileChooserDialog(
            title="Save session",
            parent=self.window,
            action=Gtk.FileChooserAction.SAVE,
            do_overwrite_confirmation=True,
        )
        dialog.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK
        )
        dialog.run()
        dialog.hide()

        try:
            filename = dialog.get_filename()
            session = self.get_session()
            fp = open(filename, "w")
            json.dump(session, fp)
            print(session)
        except Exception as e:
            print("Error :", e)
            raise ValueError("Unable to save session")

        label.set_text(f"Successfully saved to {filename}")
        infobar.set_message_type(Gtk.MessageType.INFO)
        infobar.set_revealed(True)

    def set_session(self, session):

        combobox = self.get("windows-combobox")
        from_x = self.get("from-x")
        from_y = self.get("from-y")
        to_x = self.get("to-x")
        to_y = self.get("to-y")
        actions = self.get("actions-store")
        direc = self.get("directory-chooser")
        img_type = self.get("image-types")
        exit_ = self.get("exit-check")

        name = session.get("name", None)
        if name:
            try:
                ix = list(self.windows.keys()).index(name)
            except ValueError:
                raise ValueError(f"Window : {name} not found")
            else:
                combobox.set_active(ix)

        for ent, key in [(from_x, "x1"), (from_y, "y1"), (to_x, "x2"), (to_y, "y2")]:
            val = session.get(key, None)
            if val:
                ent.set_text(str(val))

        actions_lx = session.get("actions", [])
        if actions_lx:
            actions.clear()
        for row in actions_lx:
            try:
                keyval, repeat, delay = row
                assert keyval >= 0 and repeat >= 0 and delay >= 0
            except (AssertionError, ValueError):
                raise ValueError("Invalid actions found in the session")
            else:
                actions.append([keyval, repeat, delay])

        filename = session.get("destination", None)
        if filename:
            try:
                direc.set_filename(filename)
            except Exception as e:
                print("Error :", e)
                raise ValueError("Destination directory is invalid")

        try:
            type = session["type"]
            ix = ["jpeg", "png", "tiff", "ico", "bmp"].index(type)
        except (KeyError, ValueError):
            pass
        else:
            img_type.set_active(ix)

        exit_.set_active(bool(session.get("exit", None)))

    def show_about(self, button: Gtk.Button):

        dialog = self.get("about-dialog")
        dialog.run()
        dialog.hide()

    def update_size(self, combobox: Gtk.ComboBox):

        name = combobox.get_active_text()
        if not name:
            return

        from_x = self.get("from-x")
        to_x = self.get("to-x")
        from_y = self.get("from-y")
        to_y = self.get("to-y")

        window = self.windows[name]
        xwindow = self.model.wnck_to_x(window)
        x, y, width, height = xwindow.get_geometry()

        from_x.set_text(str(x))
        from_y.set_text(str(y))
        to_x.set_text(str(width))
        to_y.set_text(str(height))
