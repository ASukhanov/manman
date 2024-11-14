"""GUI for Starting/stopping managers and servers.
Note, the command-line version of the tool can be started as:
  python -m manman.cli
"""
__version__ = 'v0.2.0 2024-11-14'# use process name for check, added shell option.
#TODO: Avoid KeyboardInterrupt while in deferredCheck()
import sys, os, time, subprocess, argparse, threading
from functools import partial
from importlib import import_module

from PyQt5 import QtWidgets, QtGui, QtCore

from . import helpers as H

Apparatus = H.list_of_apparatus()

ManCmds = ['Check','Start','Stop','Command']
Col = {'Managers':0, 'status':1, 'action':2, 'response':3}
BoldFont = QtGui.QFont("Helvetica", 14, QtGui.QFont.Bold)

qApp = QtWidgets.QApplication(sys.argv)

class MyTable(QtWidgets.QTableWidget):

    def sizeHint(self):
        hh = self.horizontalHeader()
        vh = self.verticalHeader()
        fw = self.frameWidth() * 2
        return QtCore.QSize(
            hh.length() + vh.sizeHint().width() + fw,
            vh.length() + hh.sizeHint().height() + fw)

class Main():# it may sense to subclass it from QtWidgets.QMainWindow
    tw = MyTable()
    manRow = {}
    startup = None
    timer = QtCore.QTimer()

    def __init__(self):
        Main.tw.setWindowTitle('manman')
        Main.tw.setColumnCount(4)
        Main.tw.setHorizontalHeaderLabels(Col.keys())
        wideRow(0,'Operational Managers')
        Main.tw.insertRow(1)
        sb = QtWidgets.QComboBox()
        sb.addItems(['Check All','Start All','Stop All'])
        sb.activated.connect(allManAction)
        Main.tw.setCellWidget(1, Col['action'], sb)

        operationalManager = True
        for manName in Main.startup:
            rowPosition = Main.tw.rowCount()
            if manName.startswith('tst_'):
                if operationalManager:
                    operationalManager = False
                    wideRow(rowPosition,'Test Managers')
                    rowPosition += 1
            Main.tw.insertRow(rowPosition)
            self.manRow[manName] = rowPosition
            item = QtWidgets.QTableWidgetItem(manName)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            try:    item.setToolTip(Main.startup[manName]['help'])
            except: pass
            Main.tw.setItem(rowPosition, Col['Managers'], item)
            if operationalManager:
                item.setFont(BoldFont)
                item.setBackground(QtGui.QColor('lightCyan'))
            Main.tw.setItem(rowPosition, Col['status'],
              QtWidgets.QTableWidgetItem('?'))
            sb = QtWidgets.QComboBox()
            sb.addItems(ManCmds)
            sb.activated.connect(partial(manAction,manName))
            Main.tw.setCellWidget(rowPosition, Col['action'], sb)
            Main.tw.setItem(rowPosition, Col['response'],
              QtWidgets.QTableWidgetItem(''))
        Main.tw.show()

def wideRow(rowPosition,txt):
    Main.tw.insertRow(rowPosition)
    Main.tw.setSpan(rowPosition,0,1,3)
    item = QtWidgets.QTableWidgetItem(txt)
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    item.setBackground(QtGui.QColor('lightGray'))
    item.setFont(BoldFont)
    Main.tw.setItem(rowPosition, Col['Managers'], item)

def allManAction(cmd:str):
    H.printv(f'allManAction: {cmd}')
    for manName in Main.startup:
        if manName.startswith('tst'):
            continue
        manAction(manName, cmd)

def manAction(manName, cmdObj):
    # if called on click, then cmdObj is index in ManCmds, otherwise it is a string
    cmd = cmdObj if isinstance(cmdObj,str) else ManCmds[cmdObj]
    H.printv(f'manAction: {manName, cmd}')
    cmdstart = Main.startup[manName]['cmd']    
    rowPosition = Main.manRow[manName]
    process = Main.startup[manName].get('process', f'{cmdstart}')

    if cmd == 'Check':
        H.printv(f'checking process {process} ')
        status = ['is stopped','is started'][H.is_process_running(process)]
        item = Main.tw.item(rowPosition,Col['status'])
        if not 'tst_' in manName:
            color = 'pink' if 'stop' in status else 'lightGreen'
            item.setBackground(QtGui.QColor(color))
        item.setText(status)
            
    elif cmd == 'Start':
        H.printv(f'starting {manName}')
        item = Main.tw.item(rowPosition, Col['status'])
        if not 'tst_' in manName:
            item.setBackground(QtGui.QColor('lightYellow'))
        item.setText('starting...')
        if H.is_process_running(process):
            txt = f'ERR: Manager {manName} is already running.'
            #print(txt)
            Main.tw.item(rowPosition, Col['response']).setText(txt)
            return
        path = Main.startup[manName].get('cd')
        if path:
            try:
                os.chdir(path)
            except Exception as e:
                txt = f'ERR: in chdir: {e}'
                Main.tw.item(rowPosition, Col['response']).setText(txt)
                return
            print(f'cd {path}')

        expandedCmd = os.path.expanduser(cmdstart)
        cmdlist = expandedCmd.split()
        shell = Main.startup[manName].get('shell',False)
        H.printv(f'popen: {cmdlist}, shell:{shell}')
        try:
            proc = subprocess.Popen(cmdlist, shell=shell, #close_fds=True,# env=my_env,
              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            H.printv(f'Exception: {e}') 
            Main.tw.item(rowPosition, Col['response']).setText(str(e))
            return
        Main.timer.singleShot(5000,partial(deferredCheck,(manName,rowPosition)))

    elif cmd == 'Stop':
        H.printv(f'stopping {manName}')
        cmd = f'pkill -f "{process}"'
        H.printv(f'executing: {cmd}')
        os.system(cmd)
        time.sleep(0.1)
        manAction(manName, 'Check')

    elif cmd == 'Command':
        try:
            cd = Main.startup[manName]['cd']
            cmd = f'cd {cd}; {cmdstart}'
        except Exception as e:
            cmd = cmdstart
        Main.tw.item(rowPosition, Col['response']).setText(cmd)
        return
    # Action was completed successfully, cleanup the status cell
    Main.tw.item(rowPosition, Col['response']).setText('')

def deferredCheck(args):
    manName,rowPosition = args
    manAction(manName, 'Check')
    if 'start' not in Main.tw.item(rowPosition, Col['status']).text():
        Main.tw.item(rowPosition, Col['response']).setText('Failed to start')

def main():
    parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
      epilog=f'Version {__version__}')
    parser.add_argument('-c', '--configDir', default=H.ConfigDir, help=\
      'Directory, containing apparatus configuration scripts')
    parser.add_argument('-v', '--verbose', action='count', default=0, help=\
      'Show more log messages (-vv: show even more).')
    parser.add_argument('apparatus', nargs='?', choices=Apparatus, default='TST')
    pargs = parser.parse_args()
    #pargs.log = None# disable logging fo now
    H.Constant.verbose = pargs.verbose

    # Do not do this section. Keyboard interrupt will kill all started servers!
    # arrange keyboard interrupt to kill the program
    #import signal
    #signal.signal(signal.SIGINT, signal.SIG_DFL)

    mname = 'apparatus_'+pargs.apparatus
    module = import_module(mname)
    #print(f'imported {mname} {module.__version__}')
    Main.startup = module.startup

    Main()
    allManAction('Check')

    # arrange keyboard interrupt to kill the program
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    #start GUI
    try:
        qApp.instance().exec_()
        #sys.exit(qApp.exec_())
    except Exception as e:#KeyboardInterrupt:
        # This exception never happens
        print('keyboard interrupt: exiting')
    print('Application exit')

if __name__ == '__main__':
    main()

