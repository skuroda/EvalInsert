# EvalInsert

## Overview

Plugin to execute and insert content generated from a python statement into the buffer. Note that this plugin uses the built in python function `eval`. This is not a safe method to use in general. For more on that, see this [article](http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html). This is just a general warning about the method.

## Installation

Note with either method, you may need to restart the editor for the plugin to load.

### Package Control
Installation through [Package Control](http://wbond.net/sublime_packages/package_control) is recommended. It will handle updating your packages as they become available. To install, do the following.

* In the Command Palette, enter `Package Control: Add Repository`
* In the Command Palette, enter `Package Control: Install Package`
* Search for `EvalInsert`

### Manual
Clone or copy this repository into the packages directory.

For Sublime Text 2:

* OS X: ~/Library/Application Support/Sublime Text 2/Packages/
* Windows: %APPDATA%/Roaming/Sublime Text 2/Packages/
* Linux: ~/.config/sublime-text-2/Packages/

For Sublime Text 3:

* OS X: ~/Library/Application Support/Sublime Text 3/Packages/
* Windows: %APPDATA%/Roaming/Sublime Text 3/Packages/
* Linux: ~/.config/sublime-text-3/Packages/

## Commands

`EvalInsert: EvalInsert Menu`:

Open quick panel with predefined commands.

`EvalInsert: EvalInsert Input Panel`:

Open input panel to specify command to run.

## Configuration

### Settings

`import`:

List of strings representing modules to import.

`commands`:

List of commands to display in the menu. For an details about each entry, see the  [Command Settings](https://github.com/skuroda/EvalInsert#command-settings).

### Command Settings

`name`:

The name to give the command in the menu.

`description`:

An optional description of the command. This will be displayed in the menu along with the name.

`command`:

The python command to evaluate. `_0` will be replaced with the content of the current cursor. `_n` where `n` is the nth cursor from the top. If a python script is more than a single statement, the value to be printed must be assigned to the `result` variable. In addition, `_index` will be replaced the cursor number.

### Example Commands

    {
        "name": "Multiples of 10",
        "description": "Insert multiples of 10 at each cursor starting at 0"
        "command": "_index * 10"
    }

    {
        "name": "Double cursor value",
        "command": "_0 * 2"
    }

    {
        "name": "Append firsts cursor text to all cursors",
        "command": "'_0' + '_1'"
    }
