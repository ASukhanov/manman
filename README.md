# manman
GUI for starting,stopping and checking managers (programs and servers).<br>
Usage: ```python -m manman```<br>
The following actions are defined in combobox, related to a manager:
  - **Check**
  - **Start**
  - **Stop**
  - **Command**: will display the command for starting the manager

Definition of actions, associated with an apparatus, are defined in 
python scripts code-named as apparatus_NAME.py. Scripts are imported from 
directory, specified in --configDir option.
The script should define a dictionary **startup**.

Supported keys are:
  - **'cmd'**: command which will be used to start and stop the manager,
  - **'cd'**:   directory (if needed), from where to run the cmd,
  - **'process'**: used for checking/stopping the manager to identify the manager's process. If cmd properly identifies the 
     manager, then this key is not necessary,
  - **'shell'**: some managers require shell=True option for subprocess.Popen()
  - **'help'**: it will be used as a tooltip,

## Demo
  python -m manman -c config TST

## Non-GUI usage
For command line usage:
  ```python -m manman.cli```
