# Fasd Directory Jumping for Sublime Text

The `fasd` plugin adds [fasd](https://github.com/clvv/fasd) directory jumping to Sublime Text; quickly open directories that you frequent on the command line.

A valid `fasd` installation is required.

## Installation

### Package Control

Press <kbd>cmd/ctrl</kbd> + <kbd>shift</kbd> + <kbd>p</kbd> to open the command palette.
Type `Package Control: Install Package` and press enter. Then search for `fasd`.

### Manually

Clone this repo as `fasd` into Sublime Text's `Packages` directory. (Preferences > Browse packages...)

```
git clone https://github.com/externl/sublime-fasd fasd
```

## What is fasd?

From the [fasd GitHub page](https://github.com/clvv/fasd):
> Fasd keeps track of files and directories you have accessed, so that you can quickly reference them in the command line.

## Settings

```json

  // Choices are:
  // 'best_match' — best match is used
  // 'list'       — list matches to choose from
  // 'list_all'   — search list of directories based on 'frecency'
  "mode": "list"
```

## Usage

Open the command palate and search `fasd: Jump to directory` and press enter. Depending on the `mode` setting you can either enter a directory RegEx or search a list of frequently and recently visited directories from command line `fasd` installation.

### Keybindings

<kbd>cmd/ctrl</kbd> + <kbd>shift</kbd> + <kbd>o</kbd>: jump to directory using selected `mode` setting.


