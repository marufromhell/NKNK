#!/home/maru/venv/bin/python
from importlib import reload
import sys
import os
import subprocess
shell="xonsh"
def importnknk():
    global nknk
    import nknk
    if not nknk.SUPRESSLOGS:
        print("NK: Using nknk 2.1")
        nknk.NKlog()
def run():
    nknk.cmdline() # type: ignore
arguments = sys.argv[1:]
if arguments:
    command = ' '.join(arguments)
    subprocess.run(command, executable=shell, shell=True)
    
else:
    try:
        importnknk()
        run()
    except Exception as e:
        print("NKNK: Fatal Error: ", e, "Using backup shell:", shell)
        try:
            os.system(shell)
        except Exception as e:
            print("""NK: Aww shit you fucked up, your backup shell could not be found
Using the Bourn Shell(sh)...
                  """)
            try:
                os.system("sh")
            except Exception as e:
                print("Did you rm rf / or something??? Bourn shell could not run.\nyour computer is kinda fucked, if you have no other shell installed then your computer is unrepairable\nerror: ",e)
    print("exiting...")
    while True:
        inp = input("Restart NKNK? y/lf: ")
        if inp == "y":
            importnknk()
            reload(nknk) # type: ignore
            run()
        else:
            quit()
