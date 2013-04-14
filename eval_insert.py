import sublime
import sublime_plugin
import re
import traceback


class EvalInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, eval_string=None):
        view = self.view
        window = self.view.window()
        self.region_key_prefix = "eval"
        self.settings = sublime.load_settings("EvalInsert.sublime-settings")
        cursors = view.sel()
        self.num_regions = len(cursors)

        for index in range(self.num_regions):
            view.add_regions("%s%s" % (self.region_key_prefix, index), [cursors[index]])
        if eval_string is None:
            input_view = window.show_input_panel("Enter evaluation string", "", self.execute_insert, None, self.erase_regions)
        else:
            self.execute_insert(eval_string)


    def execute_insert(self, input_string):
        view = self.view
        region_begins = []
        region_ends = []
        replace_text = []

        for match_iter in re.finditer(r"\b(_(\d+))\b", input_string):
            match_index = int(match_iter.group(2)) - 1
            if match_index != -1:
                replace_variable = view.substr(view.get_regions("%s%s" % (self.region_key_prefix, match_index))[0])
                input_string = re.sub(r"\b%s\b" % match_iter.group(1), replace_variable, input_string)


        for index in range(self.num_regions):
            temp_input = input_string
            region_key = "%s%s" % (self.region_key_prefix, index)
            cursor = view.get_regions(region_key)[0]
            replace_variable = view.substr(cursor)

            temp_input = re.sub(r"\b_0\b", replace_variable, temp_input)

            eval_global = {}
            for import_string in self.settings.get("import", []):
                eval_global[import_string] = __import__(import_string)
            result = None
            try:
                eval_statement = compile(temp_input, '<string>', 'eval')
            except SyntaxError:
                traceback.print_exc()
                print("EvalInsert: Error evaluating cursor %s" % index)
                sublime.status_message("An error occured during eval")
                result = view.substr(cursor)

            if result is None:
                result = eval(eval_statement, eval_global)
            replace_text.append(str(result))

        view.run_command("batch_replace", {"replace_text": replace_text, "region_key_prefix": self.region_key_prefix})

        self.erase_regions()

    def generate_replace_value(self, replace_variable):
        try:
            float(replace_variable)
        except:
            replace_variable = replace_variable.sub("\"", "\\\"")
            replace_variable = '"' + replace_variable + '"'
        return replace_variable

    def erase_regions(self):
        for index in range(self.num_regions):
            self.view.erase_regions("%s%s" % (self.region_key_prefix, index))


class EvalInsertMenuCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("EvalInsert.sublime-settings")
        self.quick_panel_entries = []
        self.commands = self.settings.get("commands", [])

        index = 0
        last_non_description_index = None
        for command in self.commands:
            entry = []
            entry.append(command["name"])
            if "description" in command:
                entry.append(command["description"])
                if last_non_description_index is None:
                    last_non_description_index = index
            elif last_non_description_index is not None:
                entry.append("")
            self.quick_panel_entries.append(entry)
            index += 1

        if last_non_description_index is not None:
            for i in range(last_non_description_index):
                self.quick_panel_entries[i].append("")
            self.quick_panel_entries.append(["Open insert input panel", ""])
        else:
            self.quick_panel_entries.append(["Open insert input panel"])

        self.window.show_quick_panel(self.quick_panel_entries, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        if index == len(self.commands):
            self.window.active_view().run_command("eval_insert")
        else:
            entry = self.commands[index]
            self.window.active_view().run_command("eval_insert", {"eval_string": entry["command"]})

class BatchReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, replace_text=[], region_key_prefix=""):
        for index in range(len(replace_text)):
            region_key = "%s%s" % (region_key_prefix, index)
            region = self.view.get_regions(region_key)[0]
            self.view.replace(edit, region, replace_text[index])
