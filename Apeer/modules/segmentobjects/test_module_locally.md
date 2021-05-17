**How to test your module locally**

1. First place the test files inside the correct folder.
2. Make sure the docker client has access to those folders.
3. Navigate to the GIT repository and build the docker container

```bash
docker build --rm -t test/apeer_test_segmentobj:latest .
```

3. Run the container using the input specified inside the wfe.env file:

```JSON
WFE_INPUT_JSON={"overview_image":"/input/OverViewScan.czi","filter_method":"none","filter_size":3,"threshold_method":"triangle","min_objectsize":100000,"min_holesize":1000,"WFE_output_params_file":"/output.json"}
```

4. Now run the just created docker image using:

**On Windows:**

```bash
docker run -it --rm -v %cd%\input:/input -v %cd%\output:/output --env-file wfe.env test/apeer_test_segmentobj:latest
```

**On Linux:**

```bash
docker run -it --rm -v ${pwd}/input:/input -v ${pwd}/output:/output --env-file wfe.env test/apeer_test_segmentobj:latest
```

5. Usually the result should like this:

```text
C:\Users\m1srh\Documents\Apeer_Modules\segmentobjects_ga_866c58ec-5c30-42fe-aa98-19653648a621>docker run -it --rm -v %cd%\input:/input -v %cd%\output:/output --env-file wfe.env test/apeer_test_segmentobj:latest
2021-05-15 18:30:03 [ADK:INFO] Initializing ADK v1.2.2
2021-05-15 18:30:03 [ADK:INFO] Found module's inputs to be {'overview_image': '/input/OverViewScan.czi', 'filter_method': 'none', 'filter_size': 3, 'threshold_method': 'triangle', 'min_objectsize': 100000, 'min_holesize': 1000, 'WFE_output_params_file': '/output.json'}
2021-05-15 18:30:04 [ADK:INFO] Generating new fontManager, this may take some time...
2021-05-15 18:30:05 [ADK:INFO] Outputs will be written to /output//output.json
--------------------------------------------------
FilePath :  /input/OverViewScan.czi
/usr/src/app
File exists :  True
--------------------------------------------------
...
CZI is Mosaic : True
CZI is RGB : False
No Z Dimension : 'SizeZ'
No T Dimension : 'SizeT'
No H Dimension : 'SizeH'
No I Dimension : 'SizeI'
No V Dimension : 'SizeV'
Error extracting Z Scale  : list index out of range
DetectorType not found : 'Type'
Trying to extract Scene and Well information if existing ...
WellArray Names not found : 'ArrayName'
Well ColumnIDs not found : 'Shape'
Well RowIDs not found : 'Shape'
Scales will not be rounded.
Dimensions   :  BSCMYX
Size         :  (1, 1, 1, 120, 440, 544)
Shape        :  [{'X': (0, 544), 'Y': (0, 440), 'C': (0, 1), 'M': (0, 120), 'S': (0, 1), 'B': (0, 1)}]
IsMosaic     :  True
Mosaic Shape : (1, 3216, 7400)
Well: TR1 Index S-C: 0 0 Objects: 8
100% (1 of 1) |#################################################################################################################################################################################################| Elapsed Time: 0:00:01 Time:  0:00:01 
     area   centroid-0   centroid-1  ystart  xstart  yend  xend WellId  Well_ColId  Well_RowId  S  T  Z  C  bbox_width  bbox_height  bbox_width_scaled  bbox_height_scaled  bbox_center_stageX  bbox_center_stageY
0  340964   734.098333  6482.923969     326    6124  1095  6830    TR1           0           0  0  0  0  0         706          769           3229.244            3517.406           56538.609           10538.967
1  292307   662.190249  3029.587571     365    2688   934  3373    TR1           0           0  0  0  0  0         685          569           3133.190            2602.606           40774.318           10259.953
2  306175   669.782389  4570.497346     365    4219   980  4915    TR1           0           0  0  0  0  0         696          615           3183.504            2813.010           47802.269           10365.155
3  218563   817.479637   883.520468     561     587  1056  1174    TR1           0           0  0  0  0  0         587          495           2684.938            2264.130           30940.218           10987.219
4  303429  2518.793662  4655.221132    2213    4287  2798  4991    TR1           0           0  0  0  0  0         704          585           3220.096            2675.790           48131.597           18749.297
5  357314  2559.229140  6432.040239    2233    6045  2896  6806    TR1           0           0  0  0  0  0         761          663           3480.814            3032.562           56303.048           19019.163
6  263565  2683.617282  2763.616402    2402    2444  2948  3091    TR1           0           0  0  0  0  0         647          546           2959.378            2497.404           39571.356           19524.590
7  197918  2664.852722   972.806592    2417     704  2905  1248    TR1           0           0  0  0  0  0         544          488           2488.256            2232.112           31377.035           19460.554
Done.
Write to CSV File :  OverViewScan.czi
2021-05-15 18:30:08 [ADK:INFO] Copying file "OverViewScan.ome.tiff" to "/output/OverViewScan.ome.tiff"
2021-05-15 18:30:10 [ADK:INFO] Set output "segmented_image" to "/output/OverViewScan.ome.tiff"
2021-05-15 18:30:10 [ADK:INFO] Copying file "OverViewScan_planetable.csv" to "/output/OverViewScan_planetable.csv"
2021-05-15 18:30:10 [ADK:INFO] Set output "objects_table" to "/output/OverViewScan_planetable.csv"
2021-05-15 18:30:10 [ADK:INFO] Module finalized
```

6. Commit your changes and push it to the repository. This will trigger a new build of your module.
