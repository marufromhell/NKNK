# installation
Make sure nknk is in ~/prog/
Move nksh to /usr/bin/
Run install.sh(uses dnf(fedora) but can be changed for whatever distro your on)
Change the variables in nk.py and nknk.py to be your proper home, and nknk directorys, and use whatever shell you want, I recomend xonsh or zsh.
Run nksh to start nknk


# The commandline
- if your input starts with '!' it will be executed with your nknk.Systemshell variable if you need to use a nknk variable wrap the variable in {} as if it was a f-string.
- If your input starts with '#' it will do the same as '!' but executes with sudo.
- If it starts with @ it will run as a executable. if you were in the nknk folder you'd run @nksh if in prog, you'd run @nknk/nksh

- You can type any directory and it will cd to it. (including ..)
- To autocomplete your directory or local nknk command press tab.
~ is perma-linked to your home directory.

# commands
- scmd(cmd) - this is the python backend of '!'
- cd(path) - this is the python backend of '{directory}'
- mkdir(path) - makes a directory named {path}
- pwd() - prints working directory
- clear() - clears screen
- rm(file) - deletes a file
- rmdir(folder) - recursively deletes folder contents
- pyrun(pathtopythonfile) - basically executes a python file with a full path, also works as - importing
- ls() - lists CURRENT FOLDERS contents
- curl(website) - displays a websites html.
- refresh() - re-executes nknk.
- vim(filename) - edits or creates filename and edits it in vim.
- pdv() prints defined variables
- nknkdef(command code) amends nknk with custom commands

# files.py
- read(file) - reads file contents(utf-8)
- write(filename, data) makes or replaces a file with {data}
- amend(filename, data) adds data to the end of a file, make sure {data} has a \n
- nread() frontend for read
- nwrite() frontend for write
- notepad() tui frontend for nread and write


# nknk init commands
I'd like to note that nknk is a library, not a cli, the cli is nk.
I would love to see community made cli scripts, or modified versions of nknk.

- NKlog() prints shell information
- sharks, handles args, if there are any, otherwise runs nklog, and cmdline
- make_the_sharks_swim() this is the entry point of nknk, will run sharks, if it is being run directly, if its being imported it will say log: importing script is handling init 
- incstack(int) increases system recursion limit aka stack.


# nknk structure

- nksh, the executable file that executes nk.py
- nk.py, the script to initialize nknk and provide fallback features.
- nknk.py the cli itself, init commands, and user added commands
- cmd.py the majority of cli commands
- completelib.py my readline completion library.
- cmdlist the commands that completelib uses.
- files.py my library for file handling, with no other librarys.

