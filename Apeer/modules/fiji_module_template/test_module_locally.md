**How to test your module locally**

1. First place the test files inside the correct folder.
2. Make sure the docker client has access to thoose folders.
3. Navigate to the GIT repository and build the docker container

```bash
docker build --rm -t test/apeer_test_fijimodule:latest .
```

3. Run the container using the input specified inside the wfe.env file:

```JSON
WFE_INPUT_JSON={"SCRIPT":"/Fiji.app/scripts/my_fijipyscript.py","IMAGEPATH":"/input/01_DAPI.ome.tiff","FILTERTYPE":"MEDIAN","FILTER_RADIUS":9,"WFE_output_params_file":"/output.json"}
```

4. Now run the just created docker image using:

**On Windows:**

```bash
docker run -it --rm -v %cd%\input:/input -v %cd%\output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
```

**On Linux:**

```bash
docker run -it --rm -v ${pwd}/input:/input -v ${pwd}/output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
```

5. Usually the result should like this:

```bash
C:\Apeer_Modules\fiji_module_template_b88fae21-a305-4afb-b70b-48c18efc9fa8>docker run -it --rm -v %cd%\input:/input -v %cd%\output:/output --env-file wfe.env test/apeer_test_fijimodule:latest      
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option PermSize=128m; support was removed in 8.0
Java HotSpot(TM) 64-Bit Server VM warning: Using incremental CMS is deprecated and will likely be removed in a future release
[WARNING] Not overwriting extension 'py':
        proposed = net.haesleinhuepf.clijx.te_oki.TeOkiLanguage [file:/Fiji.app/plugins/clijx-assistant_-0.4.2.21.jar
        existing = org.scijava.plugins.scripting.jython.JythonScriptLanguage [file:/Fiji.app/jars/scripting-jython-1.0.0.jar
[WARNING] Not overwriting extension 'ijm':
        proposed = net.clesperanto.macro.interpreter.ClEsperantoMacroLanguage [file:/Fiji.app/plugins/clijx-assistant_-0.4.2.21.jar
        existing = net.imagej.legacy.plugin.IJ1MacroLanguage [file:/Fiji.app/jars/imagej-legacy-0.37.4.jar
[INFO] Overriding BIOP Run Macro...; identifier: command:ch.epfl.biop.macrorunner.B_Run_Macro; jar: file:/Fiji.app/plugins/BIOP/B_Run_Macro-1.0.0-SNAPSHOT.jar
[INFO] Overriding Get Spine From Circle Rois; identifier: command:Cirlces_Based_Spine; jar: file:/Fiji.app/plugins/Max_Inscribed_Circles-1.1.0.jar
[INFO] Overriding Batch Merge Split Chip; identifier: command:de.embl.cba.bdp2.batch.LuxendoBatchMergeSplitChipCommand; jar: file:/Fiji.app/jars/fiji-plugin-bigDataProcessor2-0.4.0.jar
[INFO] Overriding Open Multiple XML/HDF5; identifier: command:de.embl.cba.bdv.utils.viewer.OpenMultipleImagesCommand; jar: file:/Fiji.app/jars/bdv-utils-0.3.5.jar
[INFO] Overriding Visualise vector field (experimental); identifier: command:net.haesleinhuepf.clijx.piv.visualisation.VisualiseVectorFieldsPlugin; jar: file:/Fiji.app/plugins/clijx_-0.30.1.21.jar
[INFO] Overriding Print text; identifier: command:de.embl.cba.cluster.commands.PrintTextCommand; jar: file:/Fiji.app/jars/fiji-slurm-0.6.0.jar
[INFO] Starting ...
[INFO] Filename               : /input/01_DAPI.ome.tiff
[INFO] Save Format used       : ome.tiff
[INFO] ------------  START IMAGE ANALYSIS ------------
[INFO] New basename for output :/output/01_DAPI
[INFO] Image Filename : /input/01_DAPI.ome.tiff
OMETiffReader initializing /input/01_DAPI.ome.tiff
Reading IFDs
Populating metadata
[INFO] ImageCount_OME : 0
[INFO] ScaleX : 0.454
[INFO] ScaleY : 0.454
[INFO] ScaleZ : 1.0
[INFO] SeriesCount_BF : 1
[INFO] SizeC : 1
[INFO] SizeT : 1
[INFO] SizeX : 1376
[INFO] SizeY : 1104
[INFO] SizeZ : 1
[INFO] is3d : False
Reading IFDs
Populating metadata
Reading IFDs
Populating metadata
[INFO] Apply Filter  : MEDIAN
[INFO] Filter Radius : 9
[INFO] Duration of Processing : 2.2557772
[INFO] Duration of saving as OME.TIFF : 1.4881731
[INFO] Writing output JSON file ...
[INFO] Done.
```

6. Commit your changes and push it to the repository. This will trigger a new build of your module.
