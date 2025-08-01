import sublime_plugin
import sublime
from os.path import relpath


class CopyPathAsPytest(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel():
            return
        point = self.view.sel()[0].begin()

        # 2. Find all regions scoped as a function in the current view
        # The 'meta.function' scope is standard for many languages
        function_regions = self.view.find_by_selector("meta.function")

        current_function_region = None
        # 3. Find which function region, if any, contains the cursor
        for r in function_regions:
            if r.contains(point):
                current_function_region = r
                break

        if not current_function_region:
            sublime.status_message("Cursor is not inside a known function.")
            return

        # 4. Within the function region, find the region for the function's name
        # The 'entity.name.function' scope is the common standard
        name_regions = self.view.find_by_selector("entity.name.function")

        current_function_name = "Unknown Function"
        for name_region in name_regions:
            # 5. Check if this name region is inside our located function region
            if current_function_region.contains(name_region):
                # 6. Extract the text of the function name
                current_function_name = self.view.substr(name_region)
                break
        filename = self.view.file_name()
        path = min(
            (relpath(filename, folder) for folder in sublime.active_window().folders()),
            key=len,
        )

        sublime.set_clipboard("inv localdev.pytest " + path + " -- -s -k " + current_function_name)
        sublime.status_message("Copied test command")

    def is_enabled(self):
        return bool(self.view.file_name() and len(self.view.file_name()) > 0)
