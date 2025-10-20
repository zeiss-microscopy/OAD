import os
from zen_api_utils.zencontrol_short import ZenTCPIP


# Define place to store the CZI file
savefolder = r"F:\Zen_Output"
ZEN_Experiment = "ZEN_API_Test.czexp"
cziname = "from_TCPIP.czi"

# open the TCP-IP connection to ZEN
zentcp = ZenTCPIP()
conn = zentcp.tcp_open_port(timeout=200, port=52757)

# define the lists of commands to be send
commandlist = [
    "from System.IO import File, Directory, Path",
    'outputfolder = r"' + savefolder + '"',
    'exp = Zen.Acquisition.Experiments.GetByName("' + ZEN_Experiment + '")',
    "exp.SetActive()",
    "img = Zen.Acquisition.Execute(exp)",
    'img.Save(Path.Combine(outputfolder, "' + cziname + '"))',
    # "img.Close()",
]

# iterate over list and send the OAD macro line-by-line
for command in commandlist:
    # print the current command and execute it
    print(command)
    rt, an = zentcp.tcp_eval_expression_and_wait_for_ok(conn, command, 200)

# finish and close TCP-IP connection to ZEN
conn.close()

czifilepath = os.path.join(savefolder, cziname)

print(f"CZI saved to: {czifilepath}")
