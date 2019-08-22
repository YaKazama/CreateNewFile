# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
"""仅适用于linux"""
import os
import sublime
import sublime_plugin
import datetime
import re


CAPTION = "Enter a path for a new file"
PACKAGE_NAME = "SublimeSimpleNewFile"
TMLP_DIR = "templates"
KEY_SYNTAX = "syntax"
KEY_FILE_EXT = "extension"
DFT_SYNTAX_KEY = ""
DFT_SYNTAX_PATH = "Packages/Text/Plain text.tmLanguage"
SETTINGS = "{}.sublime-settings".format(PACKAGE_NAME)
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path()
HOME_PATH = os.path.expanduser("~")
IS_ST3 = int(sublime.version()) >= 3000
PLATFORM = sublime.platform()
PROJECT_EXTRACT_VARIABLES = [
    'file_path', 'file_base_name', 'file_name', 'packages', 'file_extension',
    'platform', 'file', 'folder'
]


if not IS_ST3:
    raise TypeError("Please Use sublime text 3")

if PLATFORM not in ["linux", "osx"]:
    raise TypeError("Please Use Linux or OSX")


class SimpleNewFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.opts = self.get_settings()
        self.window.show_input_panel(
            CAPTION, "", self._on_done, self._on_change, self._on_cancel
        )

    def get_settings(self):
        return sublime.load_settings(SETTINGS)

    def get_path(self, f, key="root"):
        if key == "templates_path":
            _root = self.opts.get("templates_path", "default")
        elif key == "root":
            _root = self.opts.get("root", "current")
        _project = self.window.extract_variables()["folder"]
        _view = self.window.active_view().file_name()
        _current = os.path.dirname(_view) if _view else None

        if _root == "" or _root == "current":
            __root = self.opts.get("root_current_to_project_empty", False)
            # p = _current if _current else HOME_PATH
            if _current:
                p = _current
            else:
                p = HOME_PATH
                if __root:
                    p = _project if _project else HOME_PATH
        elif _root == "project":
            p = _project if _project else HOME_PATH
        elif _root == "user":
            p = os.path.join(PACKAGES_PATH, "User")
        elif _root == "default":
            if key == "templates_path":
                p = os.path.join(BASE_PATH, TMLP_DIR)
            elif key == "root":
                p = BASE_PATH
        else:
            p = HOME_PATH

        return os.path.join(p, f) if not f.startswith("/") else f

    def makedirs(self, path, mode=0o755):
        _dir = os.path.abspath(os.path.dirname(path))
        if not os.path.exists(_dir):
            os.makedirs(_dir, mode)

    def mknod(self, path, mode=0o644):
        if not os.path.exists(path):
            os.mknod(path, mode)

    def format_tag(self, c):
        if not c:
            return ""

        _code = c.replace("\r", "")

        format = self.opts.get("date_format", "%Y-%m-%d")
        date = datetime.datetime.now().strftime(format)
        if not IS_ST3:
            _code = _code.de_code("utf8")
        _code = _code.replace('${date}', date)

        _attr = self.opts.get("attrs", {})
        for k in _attr:
            _code = _code.replace('${%s}' % k, _attr.get(k, ''))

        if (self.opts.get("enable_project_variables", False) and
                hasattr(self.window, 'extract_variables')):
            _variables = self.window.extract_variables()
            for k in PROJECT_EXTRACT_VARIABLES:
                _code = _code.replace('${%s}' % k, _variables.get(k, ''))

        _code = re.sub(r"(?<!\\)\${(?!\d)", '\${', _code)
        return _code

    def get_code(self, f):
        _code = ""
        self._syntax_key = DFT_SYNTAX_KEY
        self._syntax_path = DFT_SYNTAX_PATH
        _templates = self.opts.get("templates", {})
        _extension = [x for x in f.split(".") if x != ""][-1].strip(" ")
        _syntax = self.opts.get(KEY_SYNTAX, {})
        for x in _syntax:
            for y in _syntax[x]:
                if _syntax[x][y] == _extension:
                    self._syntax_key = x
                    self._syntax_path = _syntax[x][KEY_SYNTAX]

        if _templates:
            if self._syntax_key:
                _tmpl_f = _templates.get(self._syntax_key, "")
                _tmpl_fp = self.get_path(_tmpl_f, key="templates_path")
                with open(_tmpl_fp, "r") as _f:
                    _code = _f.read()
        return self.format_tag(_code)

    def create_tab(self, fp, code):
        self.makedirs(fp)
        _view = self.window.open_file(fp)
        # 控制是否需要添加模板内容到文件中，关闭文件后参数失效
        _view.settings().set("new_file", True)
        return _view

    def set_code(self, _view, code):
        """
        参考SublimeSimpleNewFileEventListener.on_load
        """
        pass

    def set_syntax(self, view):
        view.set_syntax_file(self._syntax_path)

    def refresh_sidebar(self):
        self.window.run_command("refresh_folder_list1")

    def _on_done(self, text):
        global code
        code = ""
        # 组装路径
        fp = self.get_path(text, key="root")
        # 是否允许使用模板
        _tmpl = self.opts.get("enable_template", False)
        if _tmpl:
            code = self.get_code(fp)
        # 判断是否是 __init__.py
        _f = os.path.basename(fp)
        _init_ = self.opts.get("display_python_init_file", False)
        if _f == "__init__.py" and not _init_:
            code = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n"
            self.mknod(fp)
            with open(fp, "w") as f:
                f.write(code)
            return
        # 创建tab（view）
        _view = self.create_tab(fp, code)
        # 设置语法
        self.set_syntax(_view)
        # 设置代码
        self.set_code(_view, code)
        # 刷新
        self.refresh_sidebar()

    def _on_change(self, text):
        fp = self.get_path(text, key="root")
        self.window.status_message("Create New File: {}".format(fp))

    def _on_cancel(self):
        self.window.status_message("Create New File: Canceled")
        return


class SimpleNewFileEventListener(sublime_plugin.EventListener):
    def on_load(self, view, new_file=False):
        _flag = True if new_file else view.settings().get("new_file", False)
        if _flag:
            view.run_command("insert_snippet", {"contents": code})
            view.run_command("save")
