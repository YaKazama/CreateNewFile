# CreateNewFile

SimpleNewFile。

## 参数说明

```
{
    // "" or "current"：当前 view 所在的路径
    // "project"：Project的参数中获取 folder 定义的目录，即工程目录
    // "home": 当前用户家目录
    // "user": sublime text 3 默认定义的用户配置目录
    // "default": SimpleNewFile项目代码所在的目录
    // 若输入的 文件路径 是绝对路径，则此参数无效，返回绝对路径。
    // 上述关键字均未使用，则返回 "home"
    "root": "current",
    // 当使用 "current" 时，若 window.active_view().file_name() 为空（没有已打开的文件），是否强制将关键字置为 "project"
    // 注：使用 current 模式时，若未打开任何文件，则通过参数 root_current_to_project_empty 控制是否在当前项目中创建。可视为project的特殊情况。
    "root_current_to_project_empty": true,
    // 控制是否启用 template 添加到文件头部
    "enable_template": true,
    // "" or "current"：当前 view 所在的路径
    // "project"：Project的参数中获取 folder 定义的目录，即工程目录
    // "home": 当前用户家目录
    // "user": sublime text 3 默认定义的用户配置目录
    // "default": SimpleNewFile项目代码所在的目录，会自动添加 templates 目录
    // 即：/opt/sublime_text/Data/Packages/SimpleNewFile/templates/
    // 若输入的 文件路径 是绝对路径，则此参数无效，返回绝对路径。
    // 上述关键字均未使用，则返回 "home"
    "templates_path": "default",
    // 模板路径，相对路径会根据 templates_path 所定义的内容转换为绝对路径。
    "templates": {
        // key 与 syntax 中的名称相对应
        // 查找时，会根据 templates_path 增加前缀路径。绝对路径，则此参数无效
        "python"        : "example.tmpl",
        "markdown"      : "example.tmpl",
        "shellscript"   : "example.tmpl",
        "html"          : "example.tmpl",
        "js"            : "example.tmpl",
        "css"           : "example.tmpl",
    },
    // 自定义变量，在模板文件中需要使用 “${key}”才会生效
    "attrs": {
        "author": "ssnf",
        "email": "<example@ssnf.ssnf>",
        "version": "1.0.0",
        "link": "https://github.com/"
    },
    // 日期时间格式化字符串
    "date_format": "%Y-%m-%d %H:%M:%S",
    // 是否启用 Project 中的变量，来自于：window.extract_variables()
    "enable_project_variables": false,
    // 是否打开 __init__.py 文件，默认关闭
    "display_python_init_file": false,

    // 语法文件及文件后缀
    // 未定义，则设置为：Plain text
    "syntax": {
        // 此处的 key 必需与 “templates” 中的 key 一致。
        "python": {
            // 使用 view.settings().get('syntax') 查看当前文件所使用的语法文件
            "syntax": "Packages/Python/Python.sublime-syntax",
            // 文件后缀
            "extension": "py"
        },
        "markdown": {
            "syntax": "Packages/Markdown/Markdown.sublime-syntax",
            "extension": "md"
        },
        "shellscript": {
            "syntax": "Packages/ShellScript/Shell-Unix-Generic.tmLanguage",
            "extension": "sh"
        },
        "html": {
            "syntax": "Packages/HTML/HTML.sublime-syntax",
            "extension": "html"
        },
        "js": {
            "syntax": "Packages/JavaScript/JavaScript.sublime-syntax",
            "extension": "js"
        },
        "css": {
            "syntax": "Packages/CSS/CSS.sublime-syntax",
            "extension": "css"
        }
    }
}
```

## 安装

```
cd /opt/sublime_text/Data/Packages
git clone https://github.com/YaKazama/CreateNewFile.git
```
