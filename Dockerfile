FROM ubuntu:bionic
WORKDIR /app/program
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN apt update
RUN apt-get install -y gpg python3 python3-pip
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt update
RUN apt-get install -y python-numpy gdal-bin libgdal-dev exiftool
RUN pip3 install --upgrade pip
RUN pip3 install numpy rasterio parse srt pillow opencv-python utm
RUN apt-get install ffmpeg libsm6 libxext6  -y
ENV LANG C.UTF-8