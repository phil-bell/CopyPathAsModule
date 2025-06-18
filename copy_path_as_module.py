import sublime
import sublime_plugin
from os.path import relpath


class CopyPathAsModule(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        if len(filename) > 0:
            path = min(
                (
                    relpath(filename, folder)
                    for folder in sublime.active_window().folders()
                ),
                key=len,
            )
            path = path[:-3]
            path = path.split("/")
            path.pop(0)
            file = path.pop(-1)
            module = path[-1] + "_" + file
            path = ".".join(path)
            path = "from " + path + " import " + file + " as " + module
            sublime.set_clipboard(path)
            sublime.status_message("Copied path as module")

    def is_enabled(self):
        return bool(self.view.file_name() and len(self.view.file_name()) > 0)
