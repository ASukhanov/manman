'''manman demo. reate a startup map for starting operational servers:
    peakSimulator,
    pet_peakSimulator
    simScope

and test servers:
    tst_caproto_ioc,
    tst_sleep30

The demo servers and programs could be installed using pip:
    pip install liteserver pypeto pvplot

'''
__version__ = 'v0.2.3 2024-12-01'

import os
homeDir = os.environ['HOME']
epics_home = os.environ.get('EPICS_HOME')

help,cmd,process,cd,shell = ['help','cmd','process','cd','shell']

startup = {
#       Operational managers
'peakSimulator':{
  help: 'Liteserver, simulating peaks and noise',
  cd:   '~/github/liteServer',# This is needed if liteserver package is not installed
  cmd:  'python3 -m liteserver.device.litePeakSimulator -ilo -p9710',  
  process:  'liteserver.device.litePeakSimulator',
  },
'pet_peakSimulator':{
  help: 'Parameter editing tool for peakSimulator',
  cmd:  'python -m pypeto -aLITE localhost;9710:dev1',
  },
}
if epics_home is not None:
    startup.update({
'simScope':{
  help:'EPICS testAsynPortDriver, hosting a simulate oscilloscope',
  cd:f'{epics_home}/asyn/iocBoot/ioctestAsynPortDriver/',
  cmd:'screen -d -m -S simScope ../../bin/linux-x86_64/testAsynPortDriver st.cmd',
  process:'../../bin/linux-x86_64/testAsynPortDriver st.cmd',
  },
'pet_simScope':{
  help: 'Parameter editing tool for simScope',
  cmd:  'python3 -m pypeto -f Controls/EPICS/simScope',
  },
})
  
#       Managers for testing and debugging
startup.update({
'tst_sleep30':{help: 'sleep for 30 seconds',
  cmd:'sleep 30',
  process:'sleep 30'
  },
'tst_caproto_ioc':{
  help: 'Simple IOC for testing EPICS Channel Access functionality',
  cmd:  'python3 -m caproto.ioc_examples.simple --list-pvs',
  },
})
