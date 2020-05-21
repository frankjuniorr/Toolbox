#!/bin/bash
sudo apt install -y exiftool

git clone git://github.com/smarnach/pyexiftool.git /tmp/pyexiftool
sudo python3 /tmp/pyexiftool/setup.py install
rm -rf /tmp/pyexiftool

pip3 install -r requirements.txt