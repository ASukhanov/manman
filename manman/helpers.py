"""Helpers for manman"""
import sys, os, time, glob
import subprocess

ConfigDir = '/operations/app_store/manman'

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

def configurationDirectory():
    """Returns configuration directory"""
    argv = sys.argv
    try:    configDir = argv[argv.index('-c')+1]
    except: configDir = ConfigDir
    if os.path.exists(configDir):
        sys.path.append(configDir)
    return configDir

def list_of_apparatus():
    """Returns list of apparatus modules in configuration directory"""
    cdir = configurationDirectory()
    if not os.path.exists(cdir):
        print(f'WARNING: Local configuration directory {cdir} does not exist, will use default modules.')
        return []
    else:
        print(f'Local configurtion directory: {cdir}')
    l = glob.glob(f'{cdir}/apparatus_*.py')
    l = [i.rsplit('/',1)[1].replace('apparatus_','').replace('.py','') for i in l]
    print(f'Apparatuses: {l}')
    return l

def is_process_running(cmdstart):
    try:
        subprocess.check_output(["pgrep", '-f', cmdstart])
        return True
    except subprocess.CalledProcessError:
        return False

