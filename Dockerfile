# Use the official PyTorch image with CUDA support
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# Set environment variables to disable writing pyc files and enable offscreen mode for Qt
ENV QT_QPA_PLATFORM=xcb
ENV DISPLAY=:99

# Fixes GPU issue?
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Set the working directory
WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Update and upgrade tools
RUN apt-get update && apt-get upgrade -y

# Install build tools and essential libraries
RUN apt-get install -y \
  build-essential \
  cmake \
  git \
  pkg-config

# Install image and video I/O libraries
RUN apt-get install -y \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libavcodec-dev \
  libavformat-dev \
  libswscale-dev \
  libv4l-dev \
  v4l-utils

# Install GUI backend libraries (for full opencv-python)
RUN apt-get install -y \
  libgtk2.0-dev \
  libgtk-3-dev \
  libcanberra-gtk-module \
  libcanberra-gtk3-module

# Install other dependency libraries
RUN apt-get install -y \
  libxvidcore-dev \
  libx264-dev \
  libatlas-base-dev \
  gfortran \
  # python3-dev \
  python3-pyqt5 \
  postgresql-client


RUN apt-get update && apt-get install -y \
  libxcb-xinerama0 \
  libx11-xcb1 \
  x11-xserver-utils \
  xauth \
  xdg-utils
# Install additional Qt libraries that include the offscreen plugin
RUN apt-get update && apt-get install -y \
  xvfb \
  qt5-default \
  libqt5gui5 \
  libqt5widgets5 \
  libqt5core5a \ 
  dos2unix 

# Meta AI's segmentation tool
RUN pip install git+https://github.com/facebookresearch/segment-anything.git

# Copy the rest of the application code
COPY . .

# Ensure the entrypoint script is executable
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000 for the application
EXPOSE 8000

# Set the default command to run the application
ENTRYPOINT ["/app/entrypoint.sh"]
