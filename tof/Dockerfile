FROM resin/raspberrypi3-debian:stretch

WORKDIR /app

# Install dependencies and clean-up apt sources.
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libavresample-dev \
    libboost-all-dev \
    libcanberra-gtk* \
    libgtk2.0-dev \
    libgtk-3-dev \
    libjasper-dev \
    libjpeg-dev \
    libpng-dev \
    libffi-dev \
    libssl-dev \
    libraspberrypi-dev \
    libraspberrypi-bin \
    libswscale-dev \
    libtiff5-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    pkg-config \
    python \
    python2.7-dev \
    python3-dev \
    python3-pip \
    unzip \
    wget \
    rpi.gpio \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
# Install pip and numpy for both Python 3.
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN pip3 install azure-mgmt-eventhub

COPY spimo.py /root
COPY led.py /root
COPY VL53L0X_example.py /root
COPY VL53L0X_example_livegraph.py /root
COPY VL53L0X_TCA9548A_example.py /root
COPY VL53L0X_multi_example.py /root
COPY VL53L0X.py /root
COPY VL53L0X.pyc /root

WORKDIR /root

ENTRYPOINT python3 spimo.py
