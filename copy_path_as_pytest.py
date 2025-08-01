import sublime
import sublime_plugin
from os.path import relpath


class CopyPathAsPytest(sublime_plugin.TextCommand):
    def run(self, edit):
        relative_path = self._get_relative_path()
        function_name = self._find_current_function_name()

        command = f"inv localdev.pytest {relative_path} -- -s"
        if function_name:
            command += f" -k {function_name}"

        sublime.set_clipboard(command)
        sublime.status_message("Copied pytest command")

    def is_enabled(self):
        return bool(self.view.file_name())

    def _get_relative_path(self):
        filename = self.view.file_name()
        folders = self.view.window().folders()

        if not folders:
            return filename

        return min((relpath(filename, f) for f in folders), key=len)

    def _find_current_function_name(self):
        if not self.view.sel():
            return None

        point = self.view.sel()[0].begin()

        func_region = next(
            (r for r in self.view.find_by_selector("meta.function") if r.contains(point)), None
        )

        if not func_region:
            return None

        name_region = next(
            (
                r
                for r in self.view.find_by_selector("entity.name.function")
                if func_region.contains(r)
            ),
            None,
        )

        return self.view.substr(name_region) if name_region else None
