% Date: 17.03.2015
% Version: 1.1

% This MATLAB script demonstrates the capabilities of the .COM interface
% used to establish a connection between ZEN Blue and MATLAB.
% This connection allows to use ZEN Blue OAD Simple-API within a M-File and
% vice versa. This script only shows the 1st possibility.

% Import the ZEN Scripting into MATLAB
Zen = actxGetRunningServer('Zeiss.Micro.Scripting.ZenWrapperLM');

% Define place to store the CZI file
savefolder = 'C:\MATLAB_Output\';
% Define the experiment to be executed
ZEN_Experiment = 'ML_96_Wellplate_Observer.czexp';

% run the experiment in ZEN and save the data to the specified folder
exp = Zen.Acquisition.Experiments.GetByName(ZEN_Experiment);
img = Zen.Acquisition.Execute(exp);
% Show the image in ZEN
Zen.Application.Documents.Add(img);
% Use the correct save method - it is polymorphic ... :)
filename = [savefolder,img.Name]
img.Save_2(filename);

% Read the CZI using BioFormats
out = ReadImage6D(filename);
image6d = out{1};
metadata = out{2};

% Analyse the images - Example: Count Cells
[num, img2show, show] = AnalyzeSeries(image6d);

% Display data 
DisplayObjectNumbers(num, img2show, show);