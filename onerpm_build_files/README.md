OneRPM build files.
===========

[![ffmpeg](https://img.shields.io/badge/dependence-ffmpeg-brightgreen.svg)](https://www.ffmpeg.org/)
[![imagemagick](https://img.shields.io/badge/dependence-imagemagick-brightgreen.svg)](https://www.imagemagick.org/script/index.php)
[![so](https://img.shields.io/badge/OS-Linux-blue.svg)](https://img.shields.io/badge/OS-Linux-blue.svg)

## Description
Prepare files to upload in [oneRPM](https://www.onerpm.com/).

OneRPM need a file music master (that song that was recorded in the studio) with 44100 Hz of sample rate and a album cover art in 1400x1400 px.

So, this script convert all .mp3 files in .wav files with 44100 sample rate, and convert .jpg or .png images in 1400x1400 px images. After that, copy all files in a directory `onerpm_files`

## Use
```bash
# Download
curl -LJO https://raw.githubusercontent.com/frankjuniorr/MeusScripts/master/onerpm_build_files/onerpm_build_files.sh
chmod +x onerpm_build_files.sh

# Run
./onerpm_build_files.sh /path/of/disc
```
