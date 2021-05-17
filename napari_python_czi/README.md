# napari_zeiss

## Prerequites

In order to mak this work one needs to install the following python package [czitools](https://github.com/sebi06/czitools) inside the desired python environment:

* Clone repository or download zip.
* Avtivate the desired python environment.
* Install package via pip

```bash
git clone https://github.com/sebi06/czitools.git
cd path-to-czitools
pip install path-to-setup.py install
```

## Simple Viewing Images

Playing around with the Napari Viewer is fun. This example illustrates how to add wto widgets to the viewer.

* 1st widget can be:
  * **FileBrowser** --> Clicking on File will automatically open it inside the Viewer. The selected file is highlighted in green.
  * **TreeView** --> Clicking on a file will open it inside the Viewer
* 2nd widget is a table view, which displays some metadata of the current image

Disclaimer: This a prototype and just meant to be an example. Use at your own risk!

![Viewer with FileOpen Dialog](images/napari_filedialog.png)

![Viewer with TreeView](images/napari_treeview_lls7.png)

## Start a ZEN experiment from the Napari viewer

The Napari viewer allows to add even more interesting widgets. As a "fun project" it is possible to start a ZEN experiment from with Napari by sending ZEN python commands over TCP-IP.

For more information about controlling see: [ZEN Blue - TCP-IP Interface](https://github.com/zeiss-microscopy/OAD/tree/master/Interfaces/TCP-IP_interface)

In order to start an experiment from Napari there are a few new widgets:

* Selector for ZEN Experiments (*.czexp)
* Button **Run Experiment** to actually start a pre-configured in ZEN Blue
* Option to open an newly acquired CZI directly after the experiment is finished

![Napari Viewer with ZEN Control](images/napari_zen_tcpip1.png)

***

![Napari Viewer with ZEN Control in Action](images/Napari_simulated_CD7_TCPIP_Run_Experiment2.gif)

***

## Disclaimer

**This is an collection of scripts and tools free to use for everybody. Use it on your own risk. Especially be aware of the fact that automated stage movements might damage hardware if one starts an experiment and the the system is not setup properly. Please check everything in simulation mode first!**

By using tools tools and scripts you agree to this disclaimer.
