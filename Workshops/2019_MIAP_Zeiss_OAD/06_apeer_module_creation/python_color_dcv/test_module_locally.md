
**How to test your module locally**

1. First place the test files inside the correct folder
2. Navigate to the GIT repository and build the docker container

```bash
docker build -t sebi06/ca_test_colordcv:latest .
```

3. Run the container using the input specified inside the wfe.env file

```JSON
WFE_INPUT_JSON={"ihc_image":"/input/HED.tiff", "WFE_output_params_file":"/output.json"}
```

4. Now run the just created docker image using

```bash
docker run -it --rm -v c:\Temp\input:/input -v c:\Temp\output:/output --env-file wfe.env sebi06/ca_test_colordcv:latest
```
