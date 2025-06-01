import os
import sys
import subprocess
import shutil

"""
cmdlib
This module provides a command line functions for Python
LGPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""

def scmd(cmd):
    try:
        subprocess.run(cmd, shell=True, executable="/usr/bin/zsh") # type: ignore
    except Exception as e:
        print("Shell:", e)

def cd(path):
    os.chdir(path.replace(" ", ""))

def mkdir(path):
    try:  
        os.mkdir(path)  
    except OSError as error:  
        print(error)

def pwd():
    global current_working_directory
    current_working_directory = os.getcwd()
    print(current_working_directory)

def clear():
    _ = os.system('clear')

def rmdir(path):
    try:
        shutil.rmtree(path)
        print('Folder and its content removed')
    except:
        print('Folder not deleted')

def rm(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        rmdir(path)
    else:
        print("The file or directory does not exist") 
def pyrun(file):
    try:
        with open(file, 'r') as f:
            code = f.read()
            exec(code)
    except Exception as e:
        print("Error:", e)
    
    
def ls():
    print(os.listdir('.'))

def curl(argument):
    scmd(f"curl {argument}")

def refresh():
    r = "refreshing"
    print(r)
    os.execv(sys.argv[0], sys.argv)

def vim(a):
    scmd(f"vim {a}")