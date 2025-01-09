# Privilege-Escalation-Detection
  This is a developement project which helps in privilege escaltion prevention using python modules and enabling security in system. 
# PEG-Privilege-Escalation-Gaurd-1.0
This is a developement project which helps in privilege escaltion prevention using python modules and enabling security in system.
This project is a combination of many small python program which will run in both windows and linux .

# Requirements 
To run this python script there is a bunch of python modules required and they are
External Python Modules

    psutil
    pyautogui

Additional Module Information

    subprocess: For running system commands.
    socket: For network-related operations.
    csv: For reading and writing CSV files.
    platform: For retrieving system information.
    psutil: For system and process utilities.
    pyautogui: For GUI automation.
    webbrowser: For opening URLs in web browsers.
    time: For time-related functions.
    os: For interacting with the operating system.
    re: For regular expression operations.
    datetime: For date and time operations.

You only need to install psutil and pyautogui using pip as the other modules are part of Python's standard library.

# Installation
Modules

    psutil==5.9.4
    pyautogui==0.9.53

To install the required modules using 'pip'

    pip install -r requirements.txt

To install specific modules

    pip install <module-name>
Note : app.py is the main python script to run the tool rest of the files are the modules which are used in the main script.
To run the main python script

    python3 app.py
some modules in the python program may require root privilege to run. 
