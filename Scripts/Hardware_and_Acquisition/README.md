## Hardware and Acquistion

### FindSurface_SWAF_ActiveExp.czmac

This script is intented to be placed as a action button inside the ZEN menu bar especially when using a Celldiscoverer 7 system. The idea here is to combine the hard-based focus with the sofware focus to store the final z-value (where something should be in focus) inside the hardware focus in order to be able to relocate to that value (relative to the sample carriere surface) easily without beleaching.

The script does the following things:

* run **FindSurface** to move to the surface of the sample carrier, which is not in all cases excatly the focal plane the user wants to see

* execute a **Software Autofocus** (SWAF) based on the resulting z-psoition from **FindSurface**.

* The result of the **SWAF** will be stored as an offset inside the DF.2 and be recalled anytime via **RecallFocus**
