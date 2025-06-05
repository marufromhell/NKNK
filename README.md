# NKNK
NKNK is a Hybrid shell made with python. You can easily use it like python repl. And it has git integration. Its configurable through a yaml file. And theres a install script to configure it with a tui.  
  
Whys it not a shell? Because nknk is dependant on another shell, of your choice what shell you want. I recomend ash, or zsh for speed.

But isn't python slow? Not really in this case. NKNK isnt slow at all, usually it feels more responsive than zsh or bash when configured with themes.

# NKNK

NKNK is a Python-powered terminal interface that combines the flexibility of a Python REPL with traditional shell capabilities. It provides git integration, customizable prompts, and seamless integration with your existing shell.

## Features

- **Python REPL Integration**: Run Python commands directly in your terminal
- **Shell Command Support**: Execute regular shell commands with prefix `!` or directly with whiching enabled
- **Git Integration**: Built-in git status and branch display in prompt
- **Zoxide Support**: Quick directory navigation with `z` command
- **Customizable Prompt**: Configure user, hostname, git info, and more
- **Command Timer**: Optional execution time display for commands
- **Tab Completion**: Built-in command and path completion
- **Configuration**: YAML-based configuration with TUI installer


## Configuration Options

The configuration file is stored at `~/.config/nknk/nknk.yaml` and includes:

### System Settings
- `SUPPRESSLOGS`: Enable/disable startup logs
- `SystemShell`: Choose between zsh, bash, or xonsh
- `editor`: Default text editor for built-in commands

### Prompt Settings
- `cwd`: Show current working directory 
- `git`: Enable git integration
- `timer`: Show command execution time
- `fqdn`: Show full hostname
- `user`: Show username
- `2line`: Two-line prompt layout
- `shorthome`: Replace home path with ~

### Features
- `zoxide`: Enable directory jumping with `z` command
- `whiching`: Enable direct execution of system commands instead of using !commands

## Usage

### Basic Commands
- `!command`: Execute shell command
- `z dir`: Jump to directory (requires zoxide)
- `#command`: Execute command with sudo
- `q`: Exit NKNK
- `command` (Requires whiching to be enabled)
- Python code can be executed directly

# install
`curl -o install.py https://raw.githubusercontent.com/marufromhell/NKNK/main/install.py && python3 install.py`  
  
[![asciicast](https://asciinema.org/a/VoBZcV56wGUb1Mu0ANZv8z66V.svg)](https://asciinema.org/a/VoBZcV56wGUb1Mu0ANZv8z66V)

