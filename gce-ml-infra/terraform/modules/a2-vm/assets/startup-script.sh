#!/bin/bash

# Installing CUDA
if ! dpkg-query -W ${cuda_version}
then
    echo "Installing CUDA: " ${cuda_version}
    curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
    sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
    sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
    sudo apt update
    sudo apt -y install ${cuda_version}
else
    echo "CUDA already installed. Skipping installation"
fi

# Installing docker
if ! dpkg-query -W docker
then
    echo "Installing docker"
    curl https://get.docker.com | sh \
    && sudo systemctl start docker \
    && sudo systemctl enable docker
else
    echo "Docker already installed. Skipping installation"
fi

# Installing NVidia docker toolkit
if ! dpkg-query -W nvidia-docker
then
    echo "Installing NVIDIA Container Toolkit"
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    curl -s -L https://nvidia.github.io/nvidia-container-runtime/experimental/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list

    sudo apt-get update
    sudo apt-get install -y nvidia-docker2
    sudo systemctl restart docker
else
    echo "Nvidia docker already installed. Skipping installation"
fi

echo "Adding jupyter and unbuntu users to the docker group."

sudo usermod -a -G docker jupyter
sudo usermod -a -G docker ubuntu

echo "Authorizing jupyter and ubuntu users to access Container registry."

sudo -u jupyter gcloud auth configure-docker
sudo -u ubuntu gcloud auth configure-docker


# Installing NVidia DCGM

if ! dpkg-query -W datacenter-gpu-manager
then
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g')
   echo "deb http://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list 
   sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/7fa2af80.pub
   wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-$distribution.pin
   sudo mv cuda-$distribution.pin /etc/apt/preferences.d/cuda-repository-pin-600
   sudo apt-get update
   sudo apt-get install -y datacenter-gpu-manager
   # Enable DCGM systemd service (on reboot) and start it now
   sudo systemctl --now enable nvidia-dcgm
else
    echo "NVidia DCGM already installed. Skipping installation"
fi

echo "Startup script completed"
## Enable persistence mode
#nvidia-smi -pm 1
#

