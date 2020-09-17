from gi.repository import Gdk
from gi.repository import Gtk


def find_keyval():
    def _show_keyval(dialog, event, label):
        text = f"Key value is {event.hardware_keycode}"
        label.set_text(text)

    builder = Gtk.Builder()
    builder.add_from_file("data/assets.ui")
    dialog = builder.get_object("keyval-finder")
    label = builder.get_object("keyval-label")
    dialog.connect("key-press-event", _show_keyval, label)
    dialog.run()
    dialog.hide()


def get_coordinates():
    def _store_position(dialog, event):
        x = int(event.x)
        y = int(event.y)
        dialog.position = (x, y)
        dialog.response(0)

    builder = Gtk.Builder()
    builder.add_from_file("data/assets.ui")
    dialog = builder.get_object("position-picker")
    dialog.position = (None, None)
    dialog.connect("button-press-event", _store_position)

    dialog.realize()
    window = dialog.get_window()
    cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "crosshair")
    window.set_cursor(cursor)

    dialog.fullscreen()
    dialog.run()
    dialog.hide()
    return dialog.position


def infobar_wrapper(function):
    def wrapped(view, *args, **kwargs):
        infobar = view.get("infobar")
        label = view.get("message")
        try:
            ret = function(view, *args, **kwargs)
        except ValueError as e:
            label.set_text(str(e))
            infobar.set_message_type(Gtk.MessageType.ERROR)
            infobar.set_revealed(True)
        else:
            return ret

    return wrapped
