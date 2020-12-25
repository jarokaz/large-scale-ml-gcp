#!/bin/bash

echo "Installing CUDA"

curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt -y install ${cuda_version}


#wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
#sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
#wget https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda-repo-ubuntu2004-11-2-local_11.2.0-460.27.04-1_amd64.deb
#sudo dpkg -i cuda-repo-ubuntu2004-11-2-local_11.2.0-460.27.04-1_amd64.deb
#sudo apt-key add /var/cuda-repo-ubuntu2004-11-2-local/7fa2af80.pub
#sudo apt-get update
#sudo apt-get -y install cuda
#
## Enable persistence mode
#nvidia-smi -pm 1
#
## Install docker
#apt-get update
#apt-get install \
#    apt-transport-https \
#    ca-certificates \
#    curl \
#    software-properties-common
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
#add-apt-repository \
#   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) \
#   stable"
#apt-get update
#apt-get install -y docker-ce
#
## Install nvidia-container-runtime
#curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
#  apt-key add -
#distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
#curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
#  tee /etc/apt/sources.list.d/nvidia-docker.list
#apt-get update
#
## Install nvidia-docker2 and reload the Docker daemon configuration
#apt-get install -y nvidia-docker2
#pkill -SIGHUP dockerd
#
## add ssh key
#mkdir ~/.ssh
#
#echo "<ADD_YOUR_SSH_KEY_HERE>"  >> ~/.ssh/id_rsa_gitlab
#ssh-keyscan gitlab.com >>  ~/.ssh/known_hosts
#chmod 0400 ~/.ssh/id_rsa_gitlab
#eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_rsa_gitlab
#
## Clone project repository
#mkdir ~/datascience
#cd ~/datascience
#git clone git@gitlab.com:dice89/deep-learning-experiments.git
#