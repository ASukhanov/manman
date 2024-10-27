'''Startup commands for managers on acnlin23.
'''
import os
homeDir = os.environ['HOME']
__version__ = 'v0.0.2 2024-10-16'

help,cmd,process = ['help','cmd','process']

startup = {
#       Operational managers
'am_post': {cmd:'am post -icec-dcav', help:
  'ADO manager hor hosting parameters for other applications'},
'am_simple': {cmd:'am simple -i test', help:
  'Example of a python ADO manager'},
'peakSimulator':{cmd:'python3 -m liteserver.device.litePeakSimulator -p9710',help:
  'Lite server, simulating peaks and noise'},
'simScope':{'cd':'/home/here/cadLocal/homeAreas/caduser01/epics_32bit/asyn/iocBoot/ioctestAsynPortDriver/',
  cmd:'screen -S simScope',
  process:'../../bin/linux-x86_64/testAsynPortDriver st.cmd',
  help:'EPICS testAsynPortDriver, hosting a simulate oscilloscope'},
#       Managers for testing and debugging
'tst_caproto_ioc':  {cmd:'python3 -m caproto.ioc_examples.simple --list-pvs',help:
  'Simple IOC for testing EPICS Channel Access functionality'},
'tst_sleep30':      {cmd:'sleep 30', help: 'sleep for 30 seconds', process:'sleep 30'},
}
