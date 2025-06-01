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

# nk's not ksl
import builtins
import timeit
import files
import socket
from cmds import *
from completelib import *

SUPRESSLOGS = False
HOMEDIR = '~'
homedir = "/home/maru"
SystemShell = "/usr/bin/zsh"
nkdir = "~/prog/nknk/"
DefaultDir = nkdir
Source = f"{DefaultDir}nknk.py"

PROMPT_BASE = f"{os.getlogin()}@{socket.getfqdn()}"
###
### TEMPORARY FIX
def supress_logs():
    if SUPRESSLOGS:
        return True

    


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
    home_replace = homedir
    sudo_prefix = 'sudo '
    sudo_dot_prefix = 'sudo ./'
    
    while True:
        try:
            current_working_directory = os.getcwd()
            prompt = f"{PROMPT_BASE}{current_working_directory} ({elapsed_time})\n:"
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
                    start_time = timeit.default_timer()
                    globals().update(globals())
                    exec(command0, globals())
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

