# manman
GUI for starting,stopping and checking managers (programs and servers).<br>
Usage: ```python -m manman```<br>
The following actions are defined in combobox, related to a manager:
  - **check**
  - **start**
  - **stop**
  - **command**: will display the command for starting the manager

Definition of actions, associated with an apparatus, are defined in 
python scripts code-named as apparatus_NAME.py. Scripts are imported from 
directory, specified in --configDir option.
The script should define a dictionary **startup**.

Supported keys are:
  - **'cmd'**: command which will be used to start and stop the manager,
  - **'cd'**:   directory (if needed), from where to run the cmd,
  - **'process'**: used for stopping the manager, if cmd properly identifies the 
     manager, then this key is not necessary,
  - **'help'**: it will be used as a tooltip,

See **manman/apparatus_TST.py**.

## Non-GUI usage
For command line usage:
  ```python -m manman.cli```
