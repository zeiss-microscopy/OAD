from zen_tcpip import ZenCommands


# currently only works for the CellDiscoverer

wells = ["A1", "H1", "H12", "A12", "D6"]


def move_to_container(container_id: str):

    # define the lists of commands to be send
    commandlist = ['ZenLiveScan.MoveToContainer("' + container_id + '")']

    return commandlist


for well in wells:

    # create commandlist
    cmd_move_to_well = move_to_container(container_id=well)
    cmd = ZenCommands(cmd_move_to_well, timeout=200, port=52757)
    cmd.execute()
    print(f"Moving to well {well}")

print("Done")
