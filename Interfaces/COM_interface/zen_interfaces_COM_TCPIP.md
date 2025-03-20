

## ZEN Interfaces - COM & TCP-IP zen {#zen-interfaces---com-tcp-ip-zen .smaller .scrollable}

ZEN offers a variety of interfaces allowing to automate and customize
ZEN.

- CZI Image Format
- OAD Scripting in ZEN
- TCP-IP & COM Interface
- ZEN-API - Automate ZEN from the "outside"
- Experiment Feedback with adaptive Acquisition Engine
- ZEN Extensions (C#-based plugins)
- [pylibCZIrw](https://pypi.org/project/pylibCZIrw/)
- [czmodel](https://pypi.org/project/czmodel/)

Remark: Detailed Information and Examples: [ZEISS OAD
Github](https://github.com/zeiss-microscopy/OAD)

### ZEN Interfaces - General {#zen-interfaces---general .smaller .scrollable}

![ZEN Interfaces](./images/ZEN_Interfaces-animated_7.png){fig-align="center"}

## ZEN COM Interface {#zen-com-interface .smaller .scrollable}

- **COM (Component Object Model)** is a software architecture developed by Microsoft that allows applications to interact with each other, regardless of the language in which they were written.
- It accomplishes this by defining a way for software components to communicate through a common interface.
- In ZEN most commands available from OAD Scripting can be also addressed via the COM Interface from python.

### Registering the ZEN DLLs {#registering-the-zen-dlls .smaller .scrollable}

In order to male this work the respective ZEN DLLs need to be registered
first by executing a \*.bat file (with admin rights).

``` bat
:: regScripting_zen311.bat --> works with ZEN 3.11 or newer !!!
:: This needs to be run with administrator privileges !!!

echo off

SET DLL1="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.comhost.dll"
SET DLL2="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.LM.Scripting.comhost.dll"
SET DLL3="c:\Program Files\Carl Zeiss\ZEN 2\ZEN 2 (blue edition)\Zeiss.Micro.Scripting.Research.comhost.dll"

regsvr32.exe /u %DLL1%
regsvr32.exe /u %DLL2%
regsvr32.exe /u %DLL3%

regsvr32.exe %DLL1%
regsvr32.exe %DLL2%
regsvr32.exe %DLL3%

popd
pause
```

### COM Interface from Python {#com-interface-from-python .smaller .scrollable}

```python
import win32com.client
import os
import sys

# Define place to store the CZI file
savefolder = r"F:\Zen_Output\com_testing"

# Import the ZEN OAD Scripting into Python
Zen = win32com.client.GetActiveObject("Zeiss.Micro.Scripting.ZenWrapperLM")

ZEN_Experiment = "ZEN_API_Test.czexp"

# run the experiment in ZEN and save the data to the specified folder
exp = Zen.Acquisition.Experiments.GetByName(ZEN_Experiment)
img = Zen.Acquisition.Execute(exp)

# Use the correct save method - it is polymorphic ... :)
filename = os.path.join(savefolder, img.Name)
img.Save_2(filename)
```

## ZEN TCP-IP Interface {#zen-tcp-ip-interface .smaller .scrollable}

Even modern workstations as provided by the manufacturer are hardly able
to fulfill every single customer requirement. There is a need additional
need to

- seamlessly integrate a software package into a given workflow
- combine software packages
- integrate the ZEN software in his workflow independent of operating system and software languages or development packages

### TCP-IP Interface from Python {#tcp-ip-interface-from-python .smaller .scrollable}

Python code that sends commands to ZEN over the specified port.

```python
import os
from zencontrol_short import ZenTCPIP

# open the TCP-IP connection to ZEN
zentcp = ZenTCPIP()
conn = zentcp.tcp_open_port(timeout=200, port=52757)

# define the lists of commands to be send
commandlist = [
    "from System.IO import File, Directory, Path",
    'exp = Zen.Acquisition.Experiments.GetByName("' + "ZEN_API_Test.czexp" + '")',
    "exp.SetActive()",
    "img = Zen.Acquisition.Execute(exp)",
    'img.Save(Path.Combine(r"F:\Zen_Output", "' + "from_TCPIP.czi" + '"))',
]

# iterate over list and send the OAD macro line-by-line
for command in commandlist:
    # print the current command and execute it
    print(command)
    rt, an = zentcp.tcp_eval_expression_and_wait_for_ok(conn, command, 200)

# finish and close TCP-IP connection to ZEN
conn.close()
```

### TCP-IP - Remarks {#tcp-ip---remarks .smaller .scrollable}

Our practical experience showed that this TCP/IP approach works very
well when software packages are combined that have very little in
common. A typical example is a workflow that consists of several steps
managed by an established workflow software

- Generally the operating systems and/or the software technologies do not match
- Integration of ZEN into such situations can be done by using the TCP/IP capabilities of ZEN
- TCP/IP is a fundamental technology that is widely known and used
- Commands sent to ZEN driving the imaging software are the same that are used within a macro
- ZEN Scripts can be executed via TCP/IP by sending "run macroname"
