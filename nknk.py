# nk's not ksl
import sys
import os
import builtins
import timeit
import files
import readline #The readline module needs to be imported even if not used
import socket
from cmds import *
from completelib import *
"""
The NKNK Command line.
GPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""

SUPRESSLOGS = False
homedir = "~"
HOMEDIR = '~'
SystemShell = "/usr/bin/xonsh"
nkdir = f"~/prog/nknk/"
DefaultDir = nkdir #alias
Source = f"{DefaultDir}/nknk.py"
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

def cmdline():
    elapsed_time = 0
    user = os.getlogin()
    PCname = socket.getfqdn()
    AtNameDir = f"@{PCname}:"
    Prompt = f"{user}{AtNameDir}"
    compile()
    while True:
        try:
            current_working_directory = os.getcwd()
            user_input = input(f"{Prompt}{current_working_directory} ({elapsed_time})\n:")
            isshell = user_input.startswith('!')
            issudo = user_input.startswith('#')
            isrun = user_input.startswith('@')
            isback = user_input.startswith('..')
            isdir = os.path.isdir(user_input)
            if isshell:
                command = user_input.replace('!', '')
                try:
                    # Evaluate the command as an f-string
                    command = eval(f"f'{command}'", globals(), locals())
                except Exception as e:
                    print("\aNKNK: Error: Invalid f-string:", e)
                    continue
                scmd(command)
            elif issudo:
                command = user_input.replace('#', 'sudo ')
                scmd(command)
            elif isrun:
                command = user_input.replace('@', 'sudo ./')
                scmd(command)
            elif isdir:
                cd(user_input)
            elif isback:
                cd('..')
            elif user_input == "q":
                return 0
            else:
                try:
                    start_time = timeit.default_timer()
                    withhome = user_input.replace('~', homedir)
                    globals().update(globals())
                    exec(withhome, globals())
                    end_time = timeit.default_timer()
                    elapsed_time = round(end_time - start_time, 2)
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

#useraddedcmds