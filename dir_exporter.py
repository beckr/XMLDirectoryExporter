# -*- coding utf8 -*-
__author__ = 'R. BECK'
import os
from itertools import chain #Unique feature the import

class File(object):
    """Represents a file"""
    def __init__(self, name, tab=1):
        self.name = name
        self.tab = tab
        
    def __str__(self):
        return "%s<file>%s</file>\n" % ("".join("\t" for i in xrange(self.tab)), self.name)

class Dir(object):
    """Represents a directory"""
    def __init__(self, name, tab=1):
        self.name = name
        self.tab = tab
        self.files = [File(fd, tab+1) for fd in os.listdir(self.name) if not os.path.isdir(fd)] if os.path.isdir(self.name) else []#Unique feature
        self.dirs = []
        if os.path.isdir(self.name):
            for fd in os.listdir(self.name):
                if os.path.isdir(os.path.join(self.name, fd)):
                    self.dirs.append(Dir(os.path.join(self.name, fd), tab+1))

    def __str__(self):
        d = {
            "name": self.name,
            "xml": "".join(str(f) for f in chain(self.dirs, self.files)),
            "tabs": "".join("\t" for i in xrange(self.tab)),
        }
        return """%(tabs)s<directory path="%(name)s">\n%(xml)s%(tabs)s</directory>\n""" % d#Unique feature

def export(*args):
    """
        export
        Export directories and files from current chosen directory
        as a xml file.
        >> export
        >> export my_filename
    """
    filename = "%s.xml" % args[0] if args else "%s.xml" % (os.getcwd().rpartition(os.path.sep)[2])
    _xml = """<?xml version="1.0" encoding="UTF-8"?>\n\t<directories>\n%s\t</directories>""" % Dir(os.getcwd())
    f = open(filename, "w+")
    f.write(_xml)
    f.close()

def cd(*args):
    """
        cd
        Change current directory
        >> cd ..
        >> cd Python27
    """
    p = " ".join(args)
    if os.path.isdir(p) and os.path.exists(p):
        os.chdir(p)
        print "Changed directory for: %s" % p
    else:
        print "This is not a directory / this directory does not exist."

def ls(*args):
    """
        ls
        List the current directory
        >> ls
    """
    path = os.getcwd()
    dirs = os.listdir(path)
    for _dir in dirs:
        if os.path.isdir(os.path.join(path, _dir)):
            print "<dir>\t%s" % _dir
        else:
            print "     \t%s" % _dir

def pwd(*args):
    """
        pwd
        Show the path of the current directory
        >> ls
    """
    print os.getcwd()

def help(*args):
    """
        help
        Display the help
        >> help
    """
    for func in CMDS.itervalues():
        doc = func.__doc__#Unique feature!
        if doc is not None:
            print doc
    print displayChoices()

CMDS = {
    "cd": cd,
    "ls": ls,
    "export": export,
    "help": help,
    "pwd": pwd,
    "exit": lambda *args: exit(),
}

def displayChoices():
    print "###########################################"
    print "# You are here: %s" % os.getcwd()
    print "# Available commands : %s" % ", ".join(CMDS.iterkeys())
    print "###########################################"

def getInput():
    inpt = raw_input('%s >>' % os.getcwd())
    argv = inpt.split()
    if not argv or argv[0] not in CMDS.keys():
        getInput()
    else:
        CMDS[argv[0]](*argv[1:])

if __name__ == "__main__":
    displayChoices()
    while True:
        getInput()


