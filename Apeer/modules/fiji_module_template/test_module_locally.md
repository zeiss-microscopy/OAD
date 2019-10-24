
**How to test your module locally**

1. First place the test files inside the correct folder.
2. Make sure the docker client has access to thodse folders.
3. Navigate to the GIT repository and build the docker container

```bash
docker build --rm -t test/apeer_test_fijimodule:latest .
```

3. Run the container using the input specified inside the wfe.env file:

```JSON
WFE_INPUT_JSON={"SCRIPT":"/Fiji.app/scripts/my_fijipyscript.py","IMAGEPATH":"/input/01_DAPI.ome.tiff","FILTERTYPE":"MEDIAN","FILTER_RADIUS":9,"WFE_output_params_file":"/output.json"}
```

4. Now run the just created docker image using:

```bash
docker run -it --rm -v c:\Temp\input:/input -v c:\Temp\output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
```

5. Usually the result should like this:

```bash
C:\Users\m1srh\Documents\Apeer_Modules\fiji_module_template_b88fae21-a305-4afb-b70b-48c18efc9fa8>docker run -it --rm -v c:\Temp\input:/input -v c:\Temp\output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option PermSize=128m; support was removed in 8.0
Java HotSpot(TM) 64-Bit Server VM warning: Using incremental CMS is deprecated and will likely be removed in a future release
[INFO] Overriding BIOP Run Macro...; identifier: command:ch.epfl.biop.macrorunner.B_Run_Macro; jar: file:/Fiji.app/plugins/BIOP/B_Run_Macro-1.0.0-SNAPSHOT.jar
[INFO] Overriding Get Spine From Circle Rois; identifier: command:Cirlces_Based_Spine; jar: file:/Fiji.app/plugins/Max_Inscribed_Circles-1.1.0.jar
[INFO] Reading available sites from https://imagej.net/
[INFO] Starting ...
[INFO] Filename               : /input/01_DAPI.ome.tiff
[INFO] Save Format used       : ome.tiff
[INFO] ------------  START IMAGE ANALYSIS ------------
[INFO] New basename for output :/output/01_DAPI
[INFO] Image Filename : /input/01_DAPI.ome.tiff
[INFO] Apply Filter  : MEDIAN
[INFO] Filter Radius : 9
[INFO] Duration of whole Processing : 2.387691
[INFO] Duration of saving as OME.TIFF : 0.5261524
[INFO] Writing output JSON file ...
[INFO] Done.
```

6. Commit your changes and push it to the repository. This will trigger a new build of your module.