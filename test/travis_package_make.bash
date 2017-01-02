#!/bin/bash -xve

sudo apt-get install build-essential cmake git pkg-config
sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
sudo apt-get install libgtk2.0-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libatlas-base-dev gfortran
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
source ~/.bashrc
mkvirtualenv cv
sudo apt-get install python2.7-dev
pip install numpy
cd ~
git clone https://github.com/Itseez/opencv.git
cd opencv
git checkout 3.0.0
cd ~
git clone https://github.com/Itseez/opencv_contrib.git
cd opencv_contrib
git checkout 3.0.0
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON ..

make

sudo make install
sudo ldconfig

cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so

#sudo apt-get install libopencv-dev
sudo apt-get install ros-indigo-cv-bridge
sudo apt-get install ros-indigo-cv-camera

#sync and make
rsync -av ./ ~/catkin_ws/src/pimouse_vision_control/

#clone pimouse_ros
cd ~/catkin_ws/src/
git clone https://github.com/citueda/pimouse_ros.git

cd ~/catkin_ws
catkin_make
