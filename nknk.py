"""
The NKNK Command line.
GPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""

# todo:
# git integration
# fix how it handles commands such as "git push origin main", when using ssh. it freezes after password is entered
# make conf file
# make it less reliant on user configuration


# nk's not ksl
import builtins
import timeit
import files
import socket
import yaml
from cmds import *
from completelib import *

def load_config():
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
SUPRESSLOGS = config["system"]["SUPPRESSLOGS"]
HOMEDIR = config["system"]["HOMEDIR"]
SystemShell = config["system"]["SystemShell"]
nkdir = config["system"]["nkdir"]
DefaultEditor = config["system"]["editor"]

DefaultDir = nkdir
Source = f"{DefaultDir}/nknk.py"

ENABLE_GIT = config["prompt"]["git"]
ENABLE_TIMER = config["prompt"]["timer"]
ENABLE_FQDN = config["prompt"]["fqdn"]
ENABLE_USER = config["prompt"]["user"]
ENABLE_2LINE = config["prompt"]["2line"]
ENABLE_COLON = config["prompt"]["colon"]
if ENABLE_2LINE:
    line = "\n"
else:
    line = ""
if ENABLE_COLON:
    colon = ":"
else:
    colon = ""
# Generate prompt base if not specified in config
if ENABLE_USER and ENABLE_FQDN:
    PROMPT_BASE = f"{os.getlogin()}@{socket.getfqdn()}"
elif ENABLE_USER:
    PROMPT_BASE = os.getlogin()
elif ENABLE_FQDN:
    PROMPT_BASE = socket.getfqdn()
else:
    PROMPT_BASE = ""


def get_git_branch():
    """Get the current Git branch name."""
    try:
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return branch
    except subprocess.CalledProcessError:
        return ""  # Not a Git repository

def git_status():
    try:
        status = subprocess.check_output(
            ['git', 'status', '--porcelain'],
            stderr=subprocess.DEVNULL
        ).decode().splitlines()
        
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
    if not SUPRESSLOGS:
        print("NKNK: Log: Shell:", SystemShell)
        print("NKNK: Log: Dir:", DefaultDir)
        print("NKNK: Log: recursion limit: ",sys.getrecursionlimit())
def sharks():
    arguments = sys.argv[1:]
    if arguments:
        command = ' '.join(arguments)
        scmd(command)
    else:
        NKlog()
        cmdline()

def make_the_sharks_swim():
    if __name__=="__main__":
        sharks()
    elif not SUPRESSLOGS:
        print("NKNK: Log: Importing script is handling init")

#fun
def incstack(number):
    sys.setrecursionlimit(number)
    print(sys.getrecursionlimit())

def pdv(): #print defined variables
    script_variables = set(globals().keys())
    default_variables = set(dir(builtins))
    defined_variables = script_variables - default_variables

    for var in defined_variables:
        if var != '__builtins__' and var != 'copyright' and var != 'credits':
            print(var, "=", globals()[var])


def nknkdef(code):
    files.amend(Source, f"\n{code}")
    refresh()

def cmdline():
    elapsed_time = 0
    compile()
    
    # Pre-compile frequently used strings
    home_replace = HOMEDIR
    sudo_prefix = 'sudo '
    sudo_dot_prefix = 'sudo ./'
    
    while True:
        try:
            current_working_directory = os.getcwd()
            prompt = f"{PROMPT_BASE}{colon}{current_working_directory} {elapsed_time if ENABLE_TIMER else ''} {line}{get_git_branch() if ENABLE_GIT else ''} {git_status() if ENABLE_GIT else ''}:"
            user_input = input(prompt)

            command0 = user_input.replace('~', home_replace)
            #strips instead of replace
            if command0.startswith('!'):
                command = command0[1:]
                try:
                    command = eval(f"f'{command}'", globals(), locals())
                except Exception as e:
                    print("\aNKNK: Error: Invalid f-string:", e)
                    continue
                scmd(command)
            elif command0.startswith('#'):
                scmd(sudo_prefix + command0[1:])
            elif command0.startswith('@'):
                scmd(sudo_dot_prefix + command0[1:])
            elif os.path.isdir(command0):
                cd(command0)
            elif command0.startswith('..'):
                cd('..')
            elif command0 == "q":
                return 0
            else:
                try:
                    if ENABLE_TIMER:
                        start_time = timeit.default_timer()
                    globals().update(globals())
                    exec(command0, globals())
                    if ENABLE_TIMER:
                        elapsed_time = round(timeit.default_timer() - start_time, 2)
                except Exception as e:
                    print("NKNK: Error: Exception:", e)
                    
        except KeyboardInterrupt:
            print("\nNKNK: Log: KeyboardInterrupt")
        except EOFError:
            print("\nNKNK: Log: EOFError")
        except Exception as e:
            print("\nNKNK: Log: Exception:", e)

#args
make_the_sharks_swim()

#user added commands
#start
def viwb(x):
    if x== "j":
        scmd("sudo vim /etc/xdg/waybar/config.jsonc")
    elif x=="c":
        scmd("sudo vim /etc/xdg/waybar/style.css")
    else:
        print("j/c")
def vihl():
    scmd(f"vim ~/.config/hypr/hyprland.conf")
def vihp():
    scmd(f"vim ~/.config/hypr/hyprpaper.conf")
def vinknk():
    scmd(f"vim {Source}")
def vink():
    scmd(f"vim {nkdir}/nk.py")
def viconf():
    scmd(f"vim ~/.config/nknk/nknk.yaml")
