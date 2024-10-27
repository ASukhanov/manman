"""Helpers for manman"""
import time, glob
import subprocess

class Constant():
    verbose = 0

def printTime(): return time.strftime("%m%d:%H%M%S")
def printi(msg): print(f'inf_@{printTime()}: {msg}')
def printw(msg): print(f'WAR_@{printTime()}: {msg}')
def printe(msg): print(f'ERR_{printTime()}: {msg}')
def _printv(msg, level):
    if Constant.verbose >= level:
        print(f'dbg{level}: {msg}')
def printv(msg): _printv(msg, 1)
def printvv(msg): _printv(msg, 2)

def list_of_apparatus(rootdir):
    """Returns list of apparatus modules in folder ~/manman"""
    l = glob.glob(f'{rootdir}/apparatus_*.py')
    l = [i.rsplit('/',1)[1].replace('apparatus_','').replace('.py','') for i in l]
    return l

def is_process_running(cmdstart):
    try:
        subprocess.check_output(["pgrep", '-f', cmdstart])
        return True
    except subprocess.CalledProcessError:
        return False

