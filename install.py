print("welcome to nknk installer")
import os
import shutil
print("making config")
print('checking installs')
if os.path.exists('./nknk'):
    print('recovering failed attempt')
    os.system('rm -rf ./nknk')
def ensure_config_dir():
    config_dir = os.path.expanduser("~/.config/nknk")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
def check_git_installed():
    if shutil.which("git") == None:
        print("git not installed, exiting")
        exit()
def check_zoxide():
    if shutil.which("zoxide") == None:
        print("zoxide not installed, this will cause errors")
# credit to https://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
# i removed the windows part because i dont intend to support windows
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch() #type: ignore


getch = _Getch()
width = os.get_terminal_size().columns
#os.system("clear")


class files:
    @staticmethod
    def write(fnw, data):
        try:
            fw = open(fnw, "w", encoding="utf-8")
            fw.write(data)
            fw.close()
        except Exception as e:
            print(f"Error: {e}")
    @staticmethod
    def amend(fnw, data):
        #WILL NOT ADD NEWLINE
        try:
            with open(fnw, "r", encoding="utf-8") as read:
                existing_data = read.read()  
            with open(fnw, "w", encoding="utf-8") as write:
                write.write(existing_data + data)
        except Exception as e:
            print(f"Error: {e}")
    @staticmethod
    def touch(fnw):
        files.write(fnw, "")

def add_to_zsh_path(directory):
    zshrc_path = os.path.expanduser("~/.zshrc")
    
    # Ensure the directory exists
    if not os.path.isdir(directory):
        raise ValueError(f"The directory '{directory}' does not exist.")
    
    # Read the current .zshrc file
    if os.path.exists(zshrc_path):
        with open(zshrc_path, "r") as file:
            lines = file.readlines()
    else:
        lines = []
    path_line_found = False
    for i, line in enumerate(lines):
        if "export PATH=" in line:
            path_line_found = True
            if directory in line:
                print(f"The directory '{directory}' is already in the PATH.")
                return

            line_parts = line.split('"')
            if len(line_parts) >= 2:
                lines[i] = f'{line_parts[0]}"{line_parts[1]}:{directory}"\n'
            break
    with open(zshrc_path, "w") as file:
        file.writelines(lines)
    
    print(f"The directory '{directory}' has been added to the PATH in {zshrc_path}.")
print("Checking if git is installed")
check_git_installed()
print("Checking if config directory exists")
ensure_config_dir()
files.touch(os.path.expanduser("~/.config/nknk/nknk.yaml"))
print("config made, now writing to it")

print("Suppress Logs? (y/n)".center(width))
a=getch()
files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "system:\n")
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   SUPPRESSLOGS: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   SUPPRESSLOGS: false\n")
#os.system("clear")

print("auto configuring home directory".center(width))
a = os.path.expanduser('~')
files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), f"   HOMEDIR: \"{a}\"\n")

#os.system("clear")

shell_map = {
    "1": "xonsh",
    "2": "zsh",
    "3": "bash",
}
print("System Shell? 1) Xonsh, 2) Zsh, 3) Bash".center(width))
a=getch()
if a in shell_map:
    a = shell_map[a]
else:
    print("Invalid input, defaulting to zsh")
    a = "zsh"

files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), f"   SystemShell: \"{a}\"\n")
print(f"Added setting: SystemShell: {a} to config")

nkpath = os.path.expanduser("~/prog/nknk")
files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), f"   nkdir: \"{nkpath}\"\n")
print(f"Added setting: nkdir: {nkpath} to config")
print("What editor do you want to use? (1)Nano, (2)Vim, (3)Nvim, (4)Gedit, (5)Emacs, (6)Enter your own".center(width))
a=getch()
editor_map = {
    "1": "nano",
    "2": "vim",
    "3": "nvim",
    "4": "gedit",
    "5": "emacs"
}
if a in editor_map:
    editor = editor_map[a]
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), f"   editor: \"{editor}\"\n")
    print(f"You selected {editor}, Added setting: editor: {editor} to config")
elif a == "6":
    print("Enter your editor command:")
    editor = input()
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), f"   editor: \"{editor}\"\n")
    print(f"Added setting: editor: {editor} to config")
else:
    editor = "vim"
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   editor: \"vim\"\n")
    print("Invalid input. Added setting: editor: vim to config (default)")
os.system("clear")



print("Done with system config, Time for Customization".center(width))
files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "prompt:\n")

print("Enable command timer? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   timer: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   timer: false\n")



print("Enable current directory in prompt? Recomended (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   cwd: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   cwd: false\n")

print("Enable git integration? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   git: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   git: false\n")
#os.system("clear")

print("Enable pc name in prompt? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   fqdn: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   fqdn: false\n")
#os.system("clear")

print("Enable user name in prompt? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   user: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   user: false\n")
#os.system("clear")

print("Enable colon separator between prompt base, and current directory? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   colon: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   colon: false\n")
#os.system("clear")
print("Enable 2 line prompt? Recomended(y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   2line: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   2line: false\n")
print("Enable shorthome? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   shorthome: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   shorthome: false\n")
files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "other:\n")
os.system("clear")
print("Time for integration and other settings".center(width))
print("Enable zoxide? (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   zoxide: true\n")
    check_zoxide()
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   zoxide: false\n")
print("Enable whiching? You definitly want this. (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   whiching: true\n")
else:
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   whiching: false\n")
os.system("clear")
print("Enable full shell completions, will increase startup time by a few ms (y/n)".center(width))
a=getch()
if a == "y":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   fullshellcomps: true")
if a == "n":
    files.amend(os.path.expanduser("~/.config/nknk/nknk.yaml"), "   fullshellcomps: false")
print("All done with nknk configuration")
print("Do you want to install nknk now? (y/n)".center(width))
a=getch()
if a == "y":
    os.system("clear")
    print("Are you sure? (y/n)".center(width))
    a=getch()
    if a == "y":
        print("Do you want to use ssh or https? (1)SSH, (2)HTTPS".center(width))
        a=getch()
        if a == "1":
            print("Installing nknk via SSH...")
            if os.system("git clone git@github.com:marufromhell/NKNK.git -b main nknk") != 0:
                print("Error: Git clone failed")
                exit(1)
        elif a == "2":
            print("Installing nknk via HTTPS...")
            if os.system("git clone https://github.com/marufromhell/NKNK.git -b main nknk") != 0:
                print("Error: Git clone failed")
                exit(1)
            print('done')
        else:
            print("Invalid input, exiting...")
            exit(1)
        print('moving')
        #ensure prog exists or it fucking hates you
        os.system('mkdir ~/prog')
        os.system(f"cp -r ./nknk {nkpath}") # if path exist or not empty it is a btich with mv
        os.system('python3 -m venv ~/venv/')
        os.system(f"mv ~/venv/bin/python ~/venv/bin/nk-python")
        print("Would you like to add nknk to ZSH path? (y/n)".center(width))
        a=getch()
        if a == "y":
            path_added = True
            try:
                add_to_zsh_path(nkpath)
                print("nknk added to zsh path")
            except Exception as e:
                print(f"Error adding nknk to path: {e}")
        else:
            print("nknk not added to path, add it manually")
            path_added = False
        os.system(f"~/venv/bin/pip install -r {nkpath}/requirements.txt")
        os.system(f'chmod +x {nkpath}/nk')
        os.system("clear")
        print("Installation complete")

        print("do you want to remove install, .git, readme, LICENSE, and requirements? (y/n)".center(width))
        a=getch()
        if a == "y":
            os.system(f"rm -rf {nkpath}/.git") 
            os.system(f"rm {nkpath}/README.md")
            os.system(f"rm {nkpath}/requirements.txt")
            os.system(f"rm {nkpath}/LICENSE")
            os.system(f"rm {nkpath}/install.py")
            print("Removed .git, README.md, and requirements.txt")
        else:
            print("Not removing .git, README.md, and requirements.txt")
        print("assuming current directory is where the installer is")
        print(f"Current directory: {os.getcwd()}")
        #ensure that install.py is in the current directory
        if os.path.exists("install.py"):
            os.system("rm install.py")
        os.system('rm -rf ./nknk')
        os.system("clear")
        print("Do you want to start nk? (y/n)".center(width))
        a=getch()
        if a == "y":
            print("Starting nk...")
            os.system(f"{nkpath}/nk")
        else:
            print("You can start nk later by running the nk command in your terminal")
            print("All Done!".center(width))
            


    else:
        print("Installation cancelled".center(width))
        print("Configuration saved to ~/.config/nknk/nknk.yaml".center(width))
else:
    print("Installation cancelled".center(width))
    print("Configuration saved to ~/.config/nknk/nknk.yaml".center(width))





