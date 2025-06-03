from importlib import reload
import sys
import os
import subprocess
shell="zsh"


# for such a bulletproof script, it uses alot of type: ignore



def importnknk():
    """Import nknk and write out logs if not suppressed."""

    global nknk
    import nknk
    if not nknk.SUPRESSLOGS: # type: ignore #WHY CANT IT FUCKING FIND THE MODULE, IT WORKS SO WHY IS PYLANCE YELLING AT ME
        print("NK: Using nknk 2.1")
        nknk.NKlog() #type: ignore
def run():
    """Start the nknk shell."""
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
                os.system("/bin/sh") #assume that zsh isnt installed, and use os.system, which sends to /bin/sh
                                     #Wait sh is just a bash wrapper??? well lets just use it anyways, because the user might have a broken bashrc
            except Exception as e:
                print("Did you rm rf / or something??? Bourn shell could not run.\nyour computer is kinda fucked, if you have no other shell installed then your computer is unrepairable\nerror: ",e)
    print("exiting...") # explanation, when working on nkos it would destroy itself alot, and break the path, so if the shell was set to nk, youd be screwed
    while True:
        inp = input("Restart NKNK? y/lf: ")
        if inp == "y":
            importnknk()
            reload(nknk) # type: ignore
            run()
        else:
            quit()
