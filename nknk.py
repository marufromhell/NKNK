"""
The NKNK Command line. Passes all args to your shell as set in the config file
""""""
GPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""

# todo:
# either implement my own shell completion or steal xompletions, no disrespect to xonsh but that shit is bloated. takes longer than bash to realize a command dont exist.
# but its better out of the box than bash and i get to steal their code when im confused :)
# re add history
# windows support/ branch

#i legit made a hypr keybind to open kitty with nk
# bind = $mainMod, N, exec, $terminal nk
# the zoxide hook was completely un necisarry, but it worked as a zoxide check ig?


# nk's not ksl
import builtins
import timeit
import files
import socket
import yaml
from cmds import *
from completelib import *
import subprocess
import re

def load_config():
    """Uses yaml module to load the config file from ~/.config/nknk/nknk.yaml.
    Returns a dictionary with the configuration."""
    config_path = os.path.expanduser("~/.config/nknk/nknk.yaml")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print("NKNK: Warning: Config file not found Exiting...")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"NKNK: Error: Failed to parse config file: {e}")
        sys.exit(1)

# Load configuration
config = load_config()

# Set global variables from config
try:
    SUPRESSLOGS = config["system"]["SUPPRESSLOGS"]
    HOMEDIR = config["system"]["HOMEDIR"]
    SystemShell = config["system"]["SystemShell"]
    nkdir = config["system"]["nkdir"]
    DefaultEditor = config["system"]["editor"]

    DefaultDir = nkdir
    Source = f"{DefaultDir}/nknk.py"

    ENABLE_CWD = config["prompt"]["cwd"]
    ENABLE_GIT = config["prompt"]["git"]
    ENABLE_TIMER = config["prompt"]["timer"]
    ENABLE_FQDN = config["prompt"]["fqdn"]
    ENABLE_USER = config["prompt"]["user"]
    ENABLE_2LINE = config["prompt"]["2line"]
    ENABLE_COLON = config["prompt"]["colon"]
    ENABLE_SHORTHOME = config["prompt"]["shorthome"] # /home/user to ~ on cwd

    ENABLE_ZOXIDE = config["other"]["zoxide"]
    ENABLE_WHICHING = config["other"]["whiching"] # checks if a command exists if it isnt prefixed with a !, or a python command/var , and runs it if it does.
    ENABLE_SHCOMPS = config["other"]["fullshellcomps"]
except Exception as e:
    print(f"NKNK: Error: Failed to load configuration: {e}\nuse the installer script.")
    sys.exit(1)
###
### prompt setup
if ENABLE_2LINE:
    line = "\n"
else:
    line = ""
if ENABLE_COLON:
    colon = ":"
else:
    colon = ""
if ENABLE_USER and ENABLE_FQDN:
    PROMPT_BASE = f"{os.getlogin()}@{socket.getfqdn()}"
elif ENABLE_USER:
    PROMPT_BASE = os.getlogin()
    zoxide_available = ENABLE_ZOXIDE 

elif ENABLE_FQDN:
    PROMPT_BASE = socket.getfqdn()
else:
    PROMPT_BASE = ""
###

try:
    promptchar=config["prompt"]["promptchar"]
except Exception:
    promptchar=':'



def scmd(cmd):
    """Runs a shell command with the systemshell. Requires systemshell variable to be set."""
    try:
        subprocess.run(cmd, 
                      shell=True, 
                      executable=SystemShell,
                      text=True,
                      bufsize=1)
    except Exception as e:
        print("Shell:", e)
def get_git_branch():
    """Get the current Git branch name.

    Returns the branch name as a string, or an empty string if not in a Git repository."""
    try:
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return branch
    except subprocess.CalledProcessError:
        return ""  # Not a Git repository

def git_status():
    """Get the Git status summary.
    Returns a string summarizing the number of unstaged and untracked files."""
    
    try:
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'],stderr=subprocess.DEVNULL).decode().splitlines()
              # Count unstaged (modified) and untracked files
        unstaged = len([f for f in status if f.startswith(' M') or f.startswith('M ')])
        untracked = len([f for f in status if f.startswith('??')])
        prompt=""
        if unstaged > 0:
            prompt += f"!{unstaged} "
        if untracked > 0:
            prompt += f"?{untracked}" 
    except subprocess.CalledProcessError:
        prompt = ""
    return prompt 

def NKlog():
    """Prints current shell and directory, and recursion limit."""
    if not SUPRESSLOGS:
        print("NKNK: Log: Shell:", SystemShell)
        print("NKNK: Log: Dir:", DefaultDir)
        print("NKNK: Log: recursion limit: ",sys.getrecursionlimit())
def sharks():
    """Checks for command line arguments and runs the command if provided, otherwise calls NKlog and cmdline."""
    arguments = sys.argv[1:]
    if arguments:
        command = ' '.join(arguments)
        scmd(command)
    else:
        NKlog()
        cmdline()

def make_the_sharks_swim():
    """A funny name for checking if the script is being ran directly or imported.
    
    If ran directly, it calls sharks(). If imported, it prints a log message( if not suppresslogs)."""
    if __name__=="__main__":
        sharks()
    elif not SUPRESSLOGS:
        print("NKNK: Log: Importing script is handling init")


def incstack(number):
    """Increases the recursion limit to the specified number."""
    sys.setrecursionlimit(number)
    print(sys.getrecursionlimit())

def pdv(): #print defined variables
    script_variables = set(globals().keys())
    default_variables = set(dir(builtins))
    defined_variables = script_variables - default_variables

    for var in defined_variables:
        if var != '__builtins__' and var != 'copyright' and var != 'credits':
            return(var, "=", globals()[var])
def hand_globals_to_completer():
    commands = []
    script_variables = set(globals().keys())
    default_variables = set(dir(builtins))
    defined_variables = script_variables - default_variables

    for var in defined_variables:
        if var != '__builtins__' and var != 'copyright' and var != 'credits':
            if callable(globals()[var]):  # Check if it's a function
                commands.append(f"{var}(")
            else:
                commands.append(var)
    if ENABLE_SHCOMPS:
        shcomps = get_shell_commands()
        commands = commands + shcomps
    return commands

start_time=0 #reset so interpreter dont yell at me
def starttime():
    """Starts the timer if ENABLE_TIMER is True."""
    global start_time
    if ENABLE_TIMER:
        start_time = timeit.default_timer()
    else:
        start_time = None
elapsed_time=0 #same thing
def endtime():
    """Ends the timer and calculates elapsed time if ENABLE_TIMER is True."""
    global elapsed_time
    if ENABLE_TIMER and start_time is not None:
        elapsed_time = round(timeit.default_timer() - start_time, 2)
    else:
        elapsed_time = 0

def command_case(command):
    """ starts timer if enabled, runs the command, and prints the elapsed time if timer is enabled."""

    try:
        # Only evaluate if contains format specifiers
        #if _f_string_pattern.search(command):
        #    command = eval(f"f'{command}'", globals(), locals())  This is outdated, its better to just scmd(f"echo {python}) so that we dont mess with posix compliance
        scmd(command)
        endtime()
    except Exception as e:
        print("\aNKNK: Error: Invalid command:", e)
        return
def cmdline():
    """Checks the following conditions of user input:

1. If the input starts with 'z ', it queries zoxide for the directory and changes to it. REQUIRES ENABLE_ZOXIDE to be True.
2. If the input starts with '!', it runs the command as a shell command.
3. If the input is a directory, it changes to that directory.
4. If the input has more than one word and does not contain parentheses, it runs the command as a shell command. REQUIRES ENABLE_WHICHING to be True.
5. If the input is a valid command in the system's PATH, it runs the command as a shell command. For on-word commands.REQUIRES ENABLE_WHICHING to be True.
6. If the input starts with '#', it runs the command as a sudo command.
7. If the input is 'q', it exits the shell.
If none of these conditions are met, it tries to run the input as a Python command or variable.
If the input is invalid, it prints an error message."""
    # Pre-compile frequently used strings
    home_replace = HOMEDIR
    sudo_prefix = 'sudo '
    zoxide_available = ENABLE_ZOXIDE 

    
    compile(hand_globals_to_completer())
    
    while True:
        try:
            if ENABLE_CWD:
                if ENABLE_SHORTHOME:
                    current_working_directory = os.getcwd().replace(os.path.expanduser('~'), '~')
                else:
                    current_working_directory = os.getcwd()
            else:
                current_working_directory = ""

            prompt = f"{PROMPT_BASE}{colon}{current_working_directory}{elapsed_time if ENABLE_TIMER else ''}{line}{get_git_branch() if ENABLE_GIT else ''}{git_status() if ENABLE_GIT else ''}{promptchar}"
            command0 = input(prompt)
            starttime()
            if command0.startswith('z ' ) and ENABLE_ZOXIDE and zoxide_available: # zoxide query
                query = command0[2:].strip()
                try:
                    result = subprocess.run(['zoxide', 'query', query], capture_output=True,text=True)
                    if result.returncode == 0:
                        target_dir = result.stdout.strip()
                        cd(target_dir)
                        # add to zoxide db
                        scmd(f'zoxide add {target_dir}')
                        endtime()
                    else:
                        print(f"NKNK: Error: Zoxide: Directory not found: {query}, trying to query again... ")
                        scmd(f'z {query}')
                except Exception as e:
                    print(f"NKNK: Error: Zoxide error: {e}")
                    endtime()
                continue 
            
            elif command0.startswith('!'): #backwards compatibility
                command = command0[1:]
                command_case(command)
                endtime()

            elif os.path.isdir(command0): # if a executable and directory have the same name, cd, because its harder to manually cd than run a command
                cd(command0)
                endtime()
            elif ENABLE_WHICHING and shutil.which(command0.split()[0]) is not None and command0.split()[0] != "import": # if you use cmds like ls() but put a space in between parentheses and the command, it will run the command as a shell command. (the import thing is to make sure you can use python imports rather than import the x screenshot thing(its shit anyways so idrc about making a real solution)
                command_case(command0)
                endtime()
                    
            elif command0.startswith('#'): #sudo command
                scmd(sudo_prefix + command0[1:])
                endtime()



            elif command0 == "q":
                return 0
            
            else:
                try:
                    
                    globals().update(globals())
                    exec(command0, globals())
                    endtime()
                except Exception as e:
                    print("NKNK: Error: Exception:", e)
                    endtime()
                except KeyboardInterrupt:
                        print("\nNKNK: Log: KeyboardInterrupt")
                        endtime()
        except EOFError:
            print("\nNKNK: Log: EOFError, exiting...")
            endtime()
            break
        except Exception as e:
            print("\nNKNK: Log: Exception:", e)
            endtime()
        except KeyboardInterrupt:
                print("\nNKNK: Log: KeyboardInterrupt")
                endtime()
        

#args
make_the_sharks_swim()

#vi commands

def vinknk():
    """Opens the nknk.py file in the default editor."""
    scmd(f"{DefaultEditor} {Source}")
def vink():
    """Opens the nk.py file in the default editor."""
    scmd(f"{DefaultEditor} {nkdir}/nk.py")
def viconf():
    """Opens the nknk.yaml configuration file in the default editor."""
    scmd(f"{DefaultEditor} ~/.config/nknk/nknk.yaml")

#user added commands
# Hyprland config files
def viwb(x):
    if x== "j":
        scmd(f"sudo {DefaultEditor} /etc/xdg/waybar/config.jsonc")
    elif x=="c":
        scmd(f"sudo {DefaultEditor} /etc/xdg/waybar/style.css")
    else:
        print("j/c")
def vihl():
    scmd(f"{DefaultEditor} ~/.config/hypr/hyprland.conf")
def vihp():
    scmd(f"{DefaultEditor} ~/.config/hypr/hyprpaper.conf")
