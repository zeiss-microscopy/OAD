# The dockerfile begins with defining an image FROM which the build process starts.
# Since our module is based on python 3.0, we use python:3 as our base image.
# You can find trusted docker contains at https://store.docker.com/.
FROM python:3

# WORKDIR changes the active directory of the container to a specific location.
# In case you need to run commands from or in a particular location.
WORKDIR /usr/src/app

# COPY allows you to copy any file from host to the container.
# In this case the file requirement.txt is copied to the root directory of the container
COPY requirements.txt ./

# RUN allows you to run the command from the within the container when it's first created.
# It is used to build the image. These can be any command line instruction you wish
# if you have the dependency to support it. In our case we want to install the
# additional libraries mentioned in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Here we are copying all our files to the root directory of the container
COPY ./apeer_main.py .
COPY ./color_dcv.py .

# CMD command is similar to RUN. However unlike RUN, CMD is not executed during build, but when a container is instantiated.
# Therefore, it should be considered as an initial, default command that gets executed when container starts.
# In this example, we would like to run our python command when the container starts.
ENTRYPOINT [ "python", "./apeer_main.py" ]