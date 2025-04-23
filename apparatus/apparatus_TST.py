'''Definition of a test apparatus, running a liteServer with peak simulator.
The managers for this example could be installed with pip:
  pip install liteserver pvplot pypeto

The script should define dictionary startup.
Supported keys are:
  'cmd': command which will be used to start and stop the manager,
  'cd:   directory (if needed), from where to run the cmd,
  'process': used for stopping the manager using 'pkill -f', if cmd properly identifies the 
     manager, then this key is not necessary,
  'help': it will be used as a tooltip,
'''
import os
homeDir = os.environ['HOME']
epics_home = os.environ.get('EPICS_HOME')

__version__ = 'v0.1.4 2024-10-29'

# abbreviations:
help,cmd,process,cd = ['help','cmd','process','cd']

startup = {
#       Operational managers
# liteServer-based
'peakSimulator':{
  cmd:'python3 -m liteserver.device.litePeakSimulator -ilo -p9701',help:
  'Lite server, simulating peaks and noise'},
'plot it':{
  cmd:'python3 -m pvplot -aL:localhost;9701:dev1: x,y',help:
  'Plotting tool for peakSimulator'},
'control it':{
  cmd:'python3 -m pypeto -aLITE localhost;9701:dev1',help:
  'Spreadsheet-based control of peakSimulator parameters'},
}
if epics_home is not None:
    startup.update({
# EPICS IOCs
'simScope':{
  cd:f'{epics_home}/asyn/iocBoot/ioctestAsynPortDriver/',
  cmd:'screen -d -m -S simScope ../../bin/linux-x86_64/testAsynPortDriver st.cmd',
  process:'testAsynPortDriver st.cmd',
  help:'EPICS testAsynPortDriver, hosting a simulate oscilloscope'
},
#'tst_caproto_ioc':  {cmd:'python3 -m caproto.ioc_examples.simple --list-pvs',help:
#  'Simple IOC for testing EPICS Channel Access functionality'},

'pet_simScope':{
  help: 'Parameter editing tool for simScope',
  cmd:  'python3 -m pypeto -f Controls/EPICS/simScope',
  },
})

#       Managers for testing and debugging
startup.update({
'tst_sleep30':      {cmd:'sleep 30', help: 'sleep for 30 seconds', process:'sleep 30'},
})
