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
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip 
RUN pip install --upgrade setuptools 

# Install pip and numpy for both Python 3.
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py 


ADD odbcinst.ini /etc/odbcinst.ini
RUN apt-get install gcc
RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y

RUN pip install pyodbc
RUN pip install pyserial

COPY writetosql.py /root
COPY CRUD_pi.py /root
WORKDIR /root

ENTRYPOINT python3 writetosql.py
