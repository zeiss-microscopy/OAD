"""Explicitly runnable TCP acquisition example; importing it is inert."""

from pathlib import Path

from zen_api_utils.zen_tcpip import ZenTCPIP


def main() -> None:
    """Run the example acquisition using the local ZEN TCP interface."""
    savefolder = r"F:\Zen_Output"
    experiment_name = "ZEN_API_Test.czexp"
    czi_name = "from_TCPIP.czi"
    zen_tcp = ZenTCPIP()
    connection = zen_tcp.tcp_open_port(timeout=200, port=52757)
    commands = [
        "from System.IO import File, Directory, Path",
        f'outputfolder = r"{savefolder}"',
        f'exp = Zen.Acquisition.Experiments.GetByName("{experiment_name}")',
        "exp.SetActive()",
        "img = Zen.Acquisition.Execute(exp)",
        f'img.Save(Path.Combine(outputfolder, "{czi_name}"))',
    ]
    try:
        for command in commands:
            print(command)
            zen_tcp.tcp_eval_expression_and_wait_for_ok(connection, command, 200)
    finally:
        connection.close()
    print(f"CZI saved to: {Path(savefolder) / czi_name}")


if __name__ == "__main__":
    main()
