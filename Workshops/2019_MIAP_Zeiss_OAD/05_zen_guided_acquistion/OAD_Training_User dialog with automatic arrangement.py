#######################################################
## G E N E R A L - S H O W  U S E R  D I A L O G
##
## Macro name: OAD_Training_User dialog with automatic arrangement.py
##
## Required files: None
## Required demo files: None
##
## Required module/licence: 
##
## DESCRIPTION: Show user dialog with different controls.
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################
##
## Remove all open documents
Zen.Application.Documents.RemoveAll()
##
##

## load an image
image = Zen.Application.LoadImage()
##

## Initialize Dialog
window = ZenWindow()
window.Initialize('Guided Acquition - Version : 1')
window.Title = 'MyDialog'

## add components to dialog
window.AddLabel('Image')
window.AddImage2dView(image)
window.AddDimension(image)
window.AddFolderBrowser('destfolder','Destination folder','C:\\OAD\\Output\\CZI Images')
window.AddTextBox('tval','describe modifications:','text')
window.AddDropDown('ddval','Dropdown',['first','second','third'],1)
window.AddIntegerRange('nosamples','Number of samples',2,1,10)
window.AddIntegerRange('nosamples2','Number of samples',2,1,10)
window.AddDoubleRange('concentr','Concentration',5.5,1,6)
window.AddCheckbox('chk','Use Autofocus',False)
window.AddMultiLineTextBox('mltb','Enter multiline text','first line')
window.AddTextBlock('This is my message.')
window.RemoveContent('nosamples2')
window.SetFocus('nosamples')



## get and check results
result=window.Show()

nosamples = str(result.GetValue('nosamples'))
print(nosamples)
concentration = str(result.GetValue('concentr'))
print(concentration)


if result.Contains('ddval') and ('dval') and ('chk') and ('tval') and ('mltb'):
    allresults = format (result.GetValue('concentr'),'.2f') + '\n' + str(result.GetValue('chk')) + '\n' + str(result.GetValue('tval')) + '\n' + str(result.GetValue('mltb')) + '\n' + str(result.GetValue('destfolder')) + '\n' + str(result.GetValue('ddval'))
    Zen.Windows.Show(allresults)
else:   
    Zen.Windows.Show('Cancel')

print 'Has cancel button: ', window.HasCancelButton
print 'Has OK button: ', window.HasOkButton
print 'Has focus: ', window.FocusControl

##
#######################################################
