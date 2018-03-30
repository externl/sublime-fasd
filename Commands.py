# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import subprocess
import re


class Settings:
    def get(setting):
        return sublime.load_settings('fasd.sublime-settings').get(setting)


class FasdCommand:
    def __init__(self, directory_regex):
        self.directory_regex = directory_regex

    def run(self, flags):
        try:
            fasd_cmd = ['fasd'] + flags + [self.directory_regex]
            output = subprocess.check_output(fasd_cmd, shell=False)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            e.returncode
            if e.returncode == 1:
                return ''
            elif e.returncode == 127:
                raise Exception("fasd not found")
            raise
        except Exception as e:
            raise

    def getBestMatch(self):
        output = self.run(['--query', 'd'])
        if not output:
            return None

        matches = sorted(re.findall('^([0-9]+\.?[0-9]*)\s+(.*)', output, re.MULTILINE),
                         key=lambda t: float(t[0]), reverse=True)

        return matches[0][0]

    def getList(self):
        output = self.run(['--query', 'd'])
        if not output:
            return None

        matches = sorted(re.findall('^([0-9]+\.?[0-9]*)\s+(.*)', output, re.MULTILINE),
                         key=lambda t: float(t[0]), reverse=True)

        return [d[1] for d in matches]


class FasdJumpToDirectoryCommand(sublime_plugin.WindowCommand):
    def run(self, menu=None, action=None):
        self.mode = Settings.get('mode')
        if self.mode == 'list_all':
            self.mode_list(FasdCommand(''))
        else:
            self.window.show_input_panel("fasd: Directory regex", "", self.on_show_input_panel_done, None, None)

    def on_show_input_panel_done(self, directory_regex):
        fasd = FasdCommand(directory_regex)

        if self.mode == 'best_match':
            self.mode_best_match(fasd)
        elif self.mode == 'list':
            self.mode_list(fasd)
        else:
            raise Exception('Unknown fasd mode')

    def mode_best_match(self, fasd):
        try:
            directory = fasd.getBestMatch()
            if directory:
                self.open_directory(directory)
            else:
                sublime.message_dialog('No match for {}'.format(fasd.directory_regex))
        except Exception as e:
            sublime.error_message(str(e))

    def mode_list(self, fasd):
        try:
            directory_list = fasd.getList()
            if directory_list:
                if len(directory_list) == 1:
                    self.open_directory(directory_list[0])
                else:
                    self.show_directories(directory_list)
            else:
                sublime.message_dialog('No matches for {}'.format(fasd.directory_regex))
        except Exception as e:
            sublime.error_message(str(e))

    def on_directory_selected(self, directory):
        if directory:
            self.open_directory(directory)

    def open_directory(self, directory):
        if self.window.project_data():
            sublime.run_command('new_window')
        sublime.active_window().set_project_data({'folders': [{'path': directory}]})

        # Since everything has been successful let's actually fasd jump to the directory
        # as if we were on the command line.
        # How do we do this with fasd?
        # FasdCommand(directory).execute()

    def show_directories(self, directory_list):
        def selectedCallback(index): self.on_directory_selected(directory_list[index] if index > -1 else None)
        self.window.show_quick_panel(directory_list, selectedCallback, sublime.KEEP_OPEN_ON_FOCUS_LOST, 0, None)
