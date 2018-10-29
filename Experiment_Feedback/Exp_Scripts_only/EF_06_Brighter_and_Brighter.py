### -------------------- PreScript ---------------------------------------------- ###


from System.Diagnostics import Process

exposure = 2 # exposure time set in the acquisition parameters





### -------------------- LoopScript --------------------------------------------- ###


# get current time index and mean intensity DAPI
index = ZenService.Experiment.CurrentTimePointIndex
mean_dapi = ZenService.Analysis.Cells.RegionsIntensityMean_DAPI

#write logfile
logfile = ZenService.Xtra.System.AppendLogLine(str(index) + '\t' + str(mean_dapi))

# calculate amplification factor
index = 1 + index *0.5
# set new exposure time
ZenService.Actions.SetExposureTime(1, index*exposure)


### -------------------- PostScript --------------------------------------------- ###


# Open logfile in Notepad++
ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)

filename = ZenService.Experiment.ImageFileName[:-4] + '_Log.txt'
exeloc = 'python'
script = r'C:\TFS\Doc\3-ZIS\3-Development\Discussions\ExpFeedback\DVD_2_5\Python_Scripts\display_results_simple_intensity.py'
cmd = script + ' -f ' + filename

app = Process();
app.StartInfo.FileName = exeloc
app.StartInfo.Arguments = cmd
app.Start()