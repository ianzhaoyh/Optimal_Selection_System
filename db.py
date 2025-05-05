# db.py //database
import sys
import os

def Fstore(list, tag, no):
    tag = str(tag)
    fname = str(no)+'.txt'
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\db\\" + fname
    f = open(path, "w+")
    f.write(tag+'\n')
    for each in list:
        f.write(str(each)+'\n')
    f.close()

def Fload(no):
    exam = list()
    fname = str(no)+'.txt'
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\db\\" + fname
    f = open(path, "r")
    lines = f.readlines()[1:]
    for line in lines:
        line = line.strip()
        exam.append(line)
    f.close()
    return exam

def Fdel(no):
    fname = str(no)+'.txt'
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\db\\" + fname
    os.remove(path)

def Fget(no):
    fname = str(no)+'.txt'
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\db\\" + fname
    f = open(path, "r")
    tag = f.readline().strip()
    f.close()
    return tag

# Sample
# Fdel(1)
# Fstore(0.0, 4, [(0, 1, 2, 3), (0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4)], 1)
# Fload(0)