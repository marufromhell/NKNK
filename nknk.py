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
# allow shell curly braces somehow
# re add history
# try to allow theme scripts like starship
# DOC STRINGS


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

def init_zoxide():
    try:
        subprocess.run(['zoxide', 'init', '--hook', 'pwd'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        print("NKNK: Warning: zoxide not found. Please install zoxide first.")
        return False

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
except Exception as e:
    print(f"NKNK: Error: Failed to load configuration: {e}\nuse the installer script.")
    sys.exit(1)



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
elif ENABLE_FQDN:
    PROMPT_BASE = socket.getfqdn()
else:
    PROMPT_BASE = ""
###



def scmd(cmd):
    try:
        subprocess.run(cmd, shell=True, executable=SystemShell) # type: ignore
    except Exception as e:
        print("Shell:", e)
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
def command_case(command):
    try:

        if ENABLE_TIMER:
            start_time = timeit.default_timer()
        # Only evaluate if contains format specifiers
        if _f_string_pattern.search(command):
            command = eval(f"f'{command}'", globals(), locals())
        scmd(command)
        if ENABLE_TIMER:
            elapsed_time = round(timeit.default_timer() - start_time, 2)
    except Exception as e:
        print("\aNKNK: Error: Invalid command:", e)
        return
_f_string_pattern = re.compile(r'\{.*?\}')
def cmdline():
    elapsed_time = 0
    compile()
    # Pre-compile frequently used strings
    home_replace = HOMEDIR
    sudo_prefix = 'sudo '
    zoxide_available = init_zoxide() if ENABLE_ZOXIDE else False
    
    
    while True:
        try:
            if ENABLE_CWD:
                    
                if ENABLE_SHORTHOME:
                    current_working_directory = os.getcwd().replace(os.path.expanduser('~'), '~')
                else:
                    current_working_directory = os.getcwd()
            else:
                current_working_directory = ""


            prompt = f"{PROMPT_BASE}{colon}{current_working_directory} {elapsed_time if ENABLE_TIMER else ''} {line}{get_git_branch() if ENABLE_GIT else ''} {git_status() if ENABLE_GIT else ''}:"
            user_input = input(prompt)
            command0 = user_input
            



            if command0.startswith('z ') and ENABLE_ZOXIDE and zoxide_available:
                query = command0[2:].strip()
                try:
                    result = subprocess.run(['zoxide', 'query', query], capture_output=True,text=True)
                    if result.returncode == 0:
                        target_dir = result.stdout.strip()
                        cd(target_dir)
                        # add to zoxide db
                        scmd(f'zoxide add {target_dir}')
                    else:
                        print(f"NKNK: Error: Directory not found: {query}")
                except Exception as e:
                    print(f"NKNK: Error: Zoxide error: {e}")
                continue



            if command0.startswith('!'):
                command = command0[1:]
                command_case(command) # run the command
                

            elif os.path.isdir(command0): # if a executable and directory have the same name, cd, because its harder to manually cd than run a command
                cd(command0)

            elif len(command0.split()) > 1 and "(" not in command0: # if theres more than one word, assume its a shell command unless it has parenthesis
                command_case(command0) # run the command
            elif ENABLE_WHICHING and shutil.which(command0) is not None:
                command_case(command0)
                    
            elif command0.startswith('#'):
                scmd(sudo_prefix + command0[1:])


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
            print("\nNKNK: Log: EOFError, exiting...")
            break
        except Exception as e:
            print("\nNKNK: Log: Exception:", e)
        except KeyboardInterrupt:
                print("\nNKNK: Log: KeyboardInterrupt")
        

#args
make_the_sharks_swim()

#user added commands
#start
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
def vinknk():
    scmd(f"{DefaultEditor} {Source}")
def vink():
    scmd(f"{DefaultEditor} {nkdir}/nk.py")
def viconf():
    scmd(f"{DefaultEditor} ~/.config/nknk/nknk.yaml")
