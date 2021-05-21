# -*- coding: utf-8 -*-

#################################################################
# File        : napari_browser_cz.py
# Version     : 0.3.0
# Author      : czsrh
# Date        : 14.05.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk. Especially be aware of the fact
# that automated stage movements might damage hardware if
# one starts an experiment and the the system is not setup properly.
# Please check everything in simulation mode first!
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
#################################################################

from PyQt5.QtWidgets import (

    QHBoxLayout,
    QVBoxLayout,
    QFileSystemModel,
    QFileDialog,
    QTreeView,
    QDialogButtonBox,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QAbstractItemView,
    QComboBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QGridLayout

)

from PyQt5.QtCore import Qt, QDir
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont

import sys
import napari
import numpy as np
from aicspylibczi import CziFile
import tools.imgfile_tools as imf
import tools.fileutils as czt
import tools.napari_tools as nap
from aicsimageio import AICSImage
import dask
import dask.array as da
import zarr
import os
from zencontrol import ZenExperiment, ZenDocuments
from pathlib import Path


class FileTree(QWidget):

    def __init__(self, filter=['*.czi'], defaultfolder=r'c:\Zen_Output'):
        super(QWidget, self).__init__()

        # define filter to allowed file extensions
        #filter = ['*.czi', '*.ome.tiff', '*ome.tif' '*.tiff' '*.tif']

        # define the style for the FileTree via s style sheet
        self.setStyleSheet("""
                     QTreeView:: item {
                         background - color: rgb(38, 41, 48)
                         font - weight: bold
                     }

                     QTreeView:: item: : selected {
                         background - color: rgb(38, 41, 48)
                         color: rgb(0, 255, 0)
                     }

                     QTreeView QHeaderView: section {
                         background - color: rgb(38, 41, 48)
                         color: rgb(255, 255, 255)
                     }
                     """)

        self.model = QFileSystemModel()
        self.model.setRootPath(defaultfolder)
        self.model.setFilter(QtCore.QDir.AllDirs | QDir.Files | QtCore.QDir.NoDotAndDotDot)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(filter)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(defaultfolder))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(False)
        header = self.tree.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

        self.tree.clicked.connect(self.on_treeView_clicked)

    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        filename = self.model.fileName(indexItem)
        filepath = self.model.filePath(indexItem)

        # open the file when clicked
        print('Opening ImageFile : ', filepath)
        open_image_stack(filepath)


class OptionsWidget(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        # Create a grid layout instance
        self.grid_opt = QGridLayout()
        self.grid_opt.setSpacing(10)
        self.setLayout(self.grid_opt)

        # add checkbox to use Dask Delayed reader to the grid layout
        self.cbox_dask = QCheckBox("Use AICSImageIO Dask Reader", self)
        self.cbox_dask.setChecked(True)
        self.cbox_dask.setStyleSheet("font:bold;"
                                     "font-size: 10px;"
                                     "width :14px;"
                                     "height :14px;"
                                     )
        self.grid_opt.addWidget(self.cbox_dask, 0, 0)

        # add checkbox to open CZI after the experiment execution
        self.cbox_openczi = QCheckBox("Open CZI after Acquisition", self)
        self.cbox_openczi.setChecked(True)
        self.cbox_openczi.setStyleSheet("font:bold;"
                                        "font-size: 10px;"
                                        "width :14px;"
                                        "height :14px;"
                                        )
        self.grid_opt.addWidget(self.cbox_openczi, 1, 0)

        # add checkbox to toggle automatic scaling
        self.cbox_autoscale = QCheckBox("AutoScale per Channel (on open)", self)
        self.cbox_autoscale.setChecked(False)
        self.cbox_autoscale.setStyleSheet("font:bold;"
                                          "font-size: 10px;"
                                          "width :14px;"
                                          "height :14px;"
                                          )
        self.grid_opt.addWidget(self.cbox_autoscale, 2, 0)


class FileBrowser(QWidget):

    def __init__(self, filter="Images(*.czi)", defaultfolder=r'c:\Zen_Output'):

        super(QWidget, self).__init__()
        self.layout = QHBoxLayout(self)
        self.file_dialog = QFileDialog()
        self.file_dialog.setWindowFlags(Qt.Widget)
        self.file_dialog.setModal(False)
        self.file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        self.file_dialog.setDirectory(defaultfolder)

        # remove open and cancel button from widget
        self.buttonBox = self.file_dialog.findChild(QDialogButtonBox, "buttonBox")
        self.buttonBox.clear()

        # only show the following file types
        self.file_dialog.setNameFilter(filter)
        self.layout.addWidget(self.file_dialog)
        self.file_dialog.currentChanged.connect(open_image_stack)


class StartExperiment(QWidget):

    def __init__(self, expfiles_short,
                 savefolder=r'c:\temp',
                 default_cziname='myimage.czi'):

        super(QWidget, self).__init__()

        self.expfiles_short = expfiles_short
        self.savefolder = savefolder

        # Create a grid layout instance
        self.grid_exp = QGridLayout()
        self.grid_exp.setSpacing(10)
        self.setLayout(self.grid_exp)

        # add widgets to the grid layout
        self.expselect = QComboBox(self)
        self.expselect.addItems(self.expfiles_short)
        self.expselect.setStyleSheet("font: bold;"
                                     "font-size: 10px;"
                                     )
        self.grid_exp.addWidget(self.expselect, 0, 0)

        self.startexpbutton = QPushButton('Run Experiment')
        self.startexpbutton.setStyleSheet("font: bold;"
                                          # "background-color: red;"
                                          "font-size: 10px;"
                                          # "height: 48px;width: 120px;"
                                          )
        self.grid_exp.addWidget(self.startexpbutton, 0, 1)

        self.namelabel = QLabel(self)
        self.namelabel.setText('Save Experiment result as CZI :')
        self.namelabel.setStyleSheet("font: bold;"
                                     "font-size: 10px;"
                                     ""
                                     )
        self.grid_exp.addWidget(self.namelabel, 1, 0)

        self.nameedit = QLineEdit(self)
        self.nameedit.setText(default_cziname)
        self.nameedit.setFixedWidth(200)
        self.nameedit.setStyleSheet("font: bold;"
                                    "font-size: 10px;"
                                    )
        self.grid_exp.addWidget(self.nameedit, 1, 1)

        # Set the layout on the application's window
        self.startexpbutton.clicked.connect(self.on_click)

    def on_click(self):

        # get name of the selected experiment
        current_exp = self.expselect.currentText()
        print('Selected ZEN Experiment : ', current_exp)

        # get the desired savename
        desired_cziname = self.nameedit.text()

        # disable the button while the experiment is running
        self.startexpbutton.setText('Running ...')

        # not nice, but this "redraws" the button
        # QtCore.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        # initialize the experiment with parameters
        czexp = ZenExperiment(experiment=current_exp,
                              savefolder=self.savefolder,
                              cziname=desired_cziname)

        # start the actual experiment
        self.saved_czifilepath = czexp.startexperiment()
        print('Saved CZI : ', self.saved_czifilepath)

        # enable the button again when experiment is over
        self.startexpbutton.setEnabled(True)
        self.startexpbutton.setText('Run Experiment')

        # not nice, but this "redraws" the button
        QtWidgets.QApplication.processEvents()

        # option to use Dask Delayed reader
        use_dask = checkboxes.cbox_dask.isChecked()
        print("Use Dask Reader : ", use_dask)

        # open the just acquired CZI and show it inside napari viewer
        if self.saved_czifilepath is not None:
            open_image_stack(self.saved_czifilepath)


def open_image_stack(filepath):
    """ Open a file using AICSImageIO and display it using napari

    :param path: filepath of the image
    :type path: str
    """

    if os.path.isfile(filepath):

        # remove existing layers from napari
        viewer.layers.select_all()
        viewer.layers.remove_selected()

        # get the metadata
        metadata, add_metadata = imf.get_metadata(filepath)

        # add the global metadata and adapt the table display
        mdbrowser.update_metadata(metadata)
        mdbrowser.update_style()

        use_aicsimageio = True
        use_pylibczi = False

        # decide which tool to use to read the image
        if metadata['ImageType'] != 'czi':
            use_aicsimageio = True
        elif metadata['ImageType'] == 'czi' and metadata['czi_isMosaic'] is False:
            use_aicsimageio = True
        elif metadata['ImageType'] == 'czi' and metadata['czi_isMosaic'] is True:
            use_aicsimageio = False
            use_pylibczi = True

        # check if CZI has T or Z dimension
        hasT = False
        hasZ = False

        if 'T' in metadata['dims_aicspylibczi']:
            hasT = True
        if 'Z' in metadata['dims_aicspylibczi']:
            hasZ = True

        if use_aicsimageio:
            # get AICSImageIO object
            img = AICSImage(filepath)

            # check if the Dask Delayed Reader should be used
            if not checkboxes.cbox_dask.isChecked():
                print('Using AICSImageIO normal ImageReader.')
                all_scenes_array = img.get_image_data()
            if checkboxes.cbox_dask.isChecked():
                print('Using AICSImageIO Dask Delayed ImageReader')
                all_scenes_array = img.get_image_dask_data()

        if not use_aicsimageio and use_pylibczi is True:

            # read CZI using aicspylibczi
            czi = CziFile(filepath)

            # Get the shape of the data
            print('Dimensions   : ', czi.dims)
            print('Size         : ', czi.size)
            print('Shape        : ', czi.dims_shape())
            print('IsMoasic     : ', czi.is_mosaic())
            if czi.is_mosaic():
                print('Mosaic Size  : ', czi.read_mosaic_size())

            # get the required shape for all and single scenes
            shape_all, shape_single, same_shape = czt.get_shape_allscenes(czi, metadata)
            print('Required_Array Shape for all scenes: ', shape_all)
            for sh in shape_single:
                print('Required Array Shape for single scenes: ', sh)

            if not same_shape:
                print('No all scenes have the same shape. Exiting ...')
                sys.exit()

            #array_type = 'dask'
            array_type = 'zarr'
            #array_type = 'numpy'

            if array_type == 'zarr':

                # define array to store all channels
                print('Using aicspylibCZI to read the image (ZARR array).')

                # option 1
                all_scenes_array = zarr.create(tuple(shape_all),
                                               dtype=metadata['NumPy.dtype'],
                                               chunks=True)

                # option 2
                # all_scenes_array = zarr.open(r'c:\Temp\czi_scene_all.zarr', mode='w',
                #                            shape=shape_all,
                #                            chunks=True,
                #                            dtype=md['NumPy.dtype'])

            if array_type == 'numpy':
                print('Using aicspylibCZI to read the image (Numpy.Array).')
                all_scenes_array = np.empty(shape_all, dtype=metadata['NumPy.dtype'])

            if array_type == 'zarr' or array_type == 'numpy':

                # loop over all scenes
                for s in range(metadata['SizeS']):
                    # get the CZIscene for the current scene
                    single_scene = czt.CZIScene(czi, metadata, sceneindex=s)
                    out = czt.read_czi_scene(czi, single_scene, metadata)
                    all_scenes_array[s, :, :, :, :, :] = np.squeeze(out, axis=0)

                print(all_scenes_array.shape)

            elif array_type == 'dask':

                def dask_load_sceneimage(czi, s, md):

                    # get the CZIscene for the current scene
                    single_scene = czt.CZIScene(czi, md, sceneindex=s)
                    out = czt.read_czi_scene(czi, single_scene, md)
                    return out

                sp = shape_all[1:]

                # create dask stack of lazy image readers
                print('Using aicspylibCZI to read the image (Dask.Array) + Delayed Reading.')
                lazy_process_image = dask.delayed(dask_load_sceneimage)  # lazy reader

                lazy_arrays = [lazy_process_image(czi, s, metadata) for s in range(metadata['SizeS'])]

                dask_arrays = [
                    da.from_delayed(lazy_array, shape=sp, dtype=metadata['NumPy.dtype'])
                    for lazy_array in lazy_arrays
                ]
                # Stack into one large dask.array
                all_scenes_array = da.stack(dask_arrays, axis=0)
                print(all_scenes_array.shape)

        do_scaling = checkboxes.cbox_autoscale.isChecked()

        # show the actual image stack
        nap.show_napari(viewer, all_scenes_array, metadata,
                        blending='additive',
                        adjust_contrast=do_scaling,
                        gamma=0.85,
                        add_mdtable=False,
                        rename_sliders=True)


def get_zenfolders(zen_subfolder='Experiment Setups'):
    """Get the absolute path for a specific ZEN folder.

    :param zen_subfolder: Name of a specific subfolder, defaults to 'Experiment Setups'
    :type zen_subfolder: str, optional
    :return: specific zensubfolder path
    :rtype: str
    """

    zenfolder = None
    zensubfolder = None

    # get the user folder
    userhome = str(Path.home())

    # construct the Zen Document folder and check
    zenfolder = os.path.join(userhome, r'Documents\Carl Zeiss\ZEN\Documents')

    if os.path.isdir(zenfolder):
        zensubfolder = os.path.join(zenfolder, zen_subfolder)
    if not os.path.isdir(zenfolder):
        print('ZEN Folder: ' + zenfolder + 'not found')

    return zensubfolder


###########################################################

if __name__ == "__main__":

    # make sure this location is correct if you specify this
    #workdir = r'C:\Users\m1srh\Documents\Zen_Output'
    #workdir = r'C:\Users\m1srh\OneDrive - Carl Zeiss AG\Testdata_Zeiss'
    workdir = r'c:\Temp\input'
    #workdir = r'e:\tuxedo\zen_output'

    if os.path.isdir(workdir):
        print('SaveFolder : ', workdir, 'found.')
    if not os.path.isdir(workdir):
        print('SaveFolder : ', workdir, 'not found.')

    # specify directly or try to discover folder automatically
    # zenexpfolder = r'c:\Users\testuser\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups'
    # zenexpfolder = r'e:\Sebastian\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups'
    zenexpfolder = get_zenfolders(zen_subfolder='Experiment Setups')

    # check if the ZEN experiment folder was found
    expfiles_long = []
    expfiles_short = []

    if os.path.isdir(zenexpfolder):
        print('ZEN Experiment Setups Folder :', zenexpfolder, 'found.')
        # get lists with existing experiment files
        expdocs = ZenDocuments()
        expfiles_long, expfiles_short = expdocs.getfilenames(folder=zenexpfolder,
                                                             pattern='*.czexp')

    if not os.path.isdir(zenexpfolder):
        print('ZEN Experiment Setups Folder :', zenexpfolder, 'not found.')

    # default for saving an CZI image after acquisition
    default_cziname = 'myimage.czi'

    # decide what widget to use - 'tree' or 'dialog'
    # when using the FileTree one cannot navigate to higher levels
    fileselect = 'dialog'

    # filter for file extensions
    #filter = ['*.czi', '*.ome.tiff', '*ome.tif' '*.tiff' '*.tif']
    filter = ['*.czi']

    # start the main application
    with napari.gui_qt():

        # define the parent directory
        print('Image Directory : ', workdir)

        # initialize the napari viewer
        print('Initializing Napari Viewer ...')

        viewer = napari.Viewer()

        if fileselect == 'tree':
            # add a FileTree widget
            filetree = FileTree(filter=filter, defaultfolder=workdir)
            fbwidget = viewer.window.add_dock_widget(filetree,
                                                     name='filebrowser',
                                                     area='right')

        if fileselect == 'dialog':
            # add a FileDialog widget
            filebrowser = FileBrowser(defaultfolder=workdir)
            fbwidget = viewer.window.add_dock_widget(filebrowser,
                                                     name='filebrowser',
                                                     area='right')

        # create the widget elements to be added to the napari viewer

        # table for the metadata and for options
        mdbrowser = nap.TableWidget()
        checkboxes = OptionsWidget()

        # widget to start an experiment in ZEN remotely
        expselect = StartExperiment(expfiles_short,
                                    savefolder=workdir,
                                    default_cziname=default_cziname)

        # add widget to activate the dask delayed reading
        cbwidget = viewer.window.add_dock_widget(checkboxes,
                                                 name='checkbox',
                                                 area='bottom')

        # add the Table widget for the metadata
        mdwidget = viewer.window.add_dock_widget(mdbrowser,
                                                 name='mdbrowser',
                                                 area='right')

        # add the Experiment Selector widget
        expwidget = viewer.window.add_dock_widget(expselect,
                                                  name='expselect',
                                                  area='bottom')
