from os.path import relpath

import sublime
import sublime_plugin


class CopyPathAsModule(sublime_plugin.TextCommand):
    def run(self, edit):
        _filename = self.view.file_name()
        _path = min(
            (relpath(_filename, _folder) for _folder in sublime.active_window().folders()),
            key=len,
        )
        _path = _path[:-3]
        _path = _path.split("/")
        _path.pop(0)
        file = _path.pop(-1)

        if file.startswith("_"):
            _as = _path[-1] + "_" + _path[-2]
            _module = _path.pop()
            _path = ".".join(_path)
            _import = "from " + _path + " import " + _module + " as " + _as
            sublime.set_clipboard(_import)
        else:
            _as = _path[-1] + "_" + file
            _path = ".".join(_path)
            _import = "from " + _path + " import " + file + " as " + _as
            sublime.set_clipboard(_import)
            sublime.status_message("Copied path as module")

    def is_enabled(self):
        return bool(self.view.file_name() and len(self.view.file_name()) > 0)
