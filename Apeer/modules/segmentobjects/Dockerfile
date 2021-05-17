FROM continuumio/miniconda3

# WORKDIR changes the active directory of the container to a specific location.
# In case you need to run commands from or in a particular location.
WORKDIR /usr/src/app

# Create the environment:

# read here for details:
# https://medium.com/@chadlagore/conda-environments-with-docker-82cdc9d25754
# https://pythonspeed.com/articles/activate-conda-dockerfile/#working

COPY conda_env_ia_czi.yml .
COPY requirements.txt .
RUN conda env create -f conda_env_ia_czi.yml

# or this method seems to work as well
# RUN echo "source activate imageanalysis_czi" > ~/.bashrc
# ENV PATH /opt/conda/envs/env/bin:$PATH

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "imageanalysis_czi", "/bin/bash", "-c"]

# Here we are copying all our files to the root directory of the container
COPY apeer_main.py .
COPY segment_objects.py .
# copy a complete folder by using ADD
ADD tools tools
COPY module_specification.json .

# Include this, if you need Matplotlib to generate the output image
RUN mkdir -p /root/.config/matplotlib
RUN echo "backend : Qt5Agg" > /root/.config/matplotlib/matplotlibrc

# mount volumes
VOLUME [ "/input", "/output" ]

# code to run when container is started:
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "imageanalysis_czi", "python", "apeer_main.py"]

