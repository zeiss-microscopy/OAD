### -------------------- PreScript ---------------------------------------------- ###


from System.Diagnostics import Process


### -------------------- LoopScript --------------------------------------------- ###


# Retrieve the current image acquisition time. This will be different for every frame!
index = ZenService.Analysis.Cells.ImageIndexTime

# get the number of cells for the current frame
cn = ZenService.Analysis.Cells.RegionsCount

# write data to log file: index and number of cells 
logfile = ZenService.Xtra.System.AppendLogLine(str(index) + "\t" + str(cn))


### -------------------- PostScript --------------------------------------------- ###


# Open logfile in Notepad++
ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)

filename = ZenService.Experiment.ImageFileName[:-4] + '_Log.txt'
exeloc = 'python'
script = r'C:\TFS\Doc\3-ZIS\3-Development\Discussions\ExpFeedback\DVD_2_5\Python_Scripts\display_results_simple.py'
cmd = script + ' -f ' + filename

## start Python Option 1
#ZenService.Xtra.System.ExecuteExternalProgram(script, ' -f ' + filename)

## start Python Option 2
app = Process();
app.StartInfo.FileName = exeloc
app.StartInfo.Arguments = cmd
app.Start()