#!/usr/bin/env bash

# linux:$ ./bin/install.sh

# installation sur un env. : ubuntu 18.10
echo "####### Installation des dependances..."

# pip3
sudo apt-get install -y python3-pip
# FIXME : libav-tools failed !
sudo apt-get install -y \
    python3-numpy libsdl-image1.2-dev \
    libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
    libfreetype6-dev
# pygame
sudo pip3 install -q pygame

echo "####### Fin..."
