# Use exiszing image: Pull base Fiji baseimage from docker hub
FROM czsip/fiji_linux64_baseimage:latest

# add Fiji to path
ENV PATH $PATH:/Fiji.app/

# mount volumes
VOLUME [ "/input", "/output" ]

# copy other scripts or files (when required)
COPY ./my_fijipyscript.py /Fiji.app/scripts

# define the starting script
COPY ./start.sh /
ENTRYPOINT ["sh","./start.sh"]