from gi.repository import GLib

options = [
    (
        "filename",
        ord("f"),
        GLib.OptionFlags.NONE,
        GLib.OptionArg.STRING,
        "Edit existing capture instead of making new one",
        "A valid session file",
    ),
    (
        "quick",
        ord("q"),
        GLib.OptionFlags.NONE,
        GLib.OptionArg.NONE,
        "Immediately executes the actions after launching GUI",
        None,
    ),
]
