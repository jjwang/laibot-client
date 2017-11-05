
# How to install PocketSphinx on a RPi
## by [tyler]
## Download the latest version of sphinxbase and pocketsphinx
* You can find the downloads here: http://cmusphinx.sourceforge.net/wiki/download.
>       wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz
>       wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz
## Extract the files into separate directories
>       tar -xzvf sphinxbase.tar.gz
>       tar -xzvf pocketsphinx.tar.gz
## Install bison, ALSA, and swig
>       sudo apt-get install bison libasound2-dev swig
## Compile sphinxbase
>       cd sphinxbase-5prealpha
>       ./configure --enable-fixed
>       makesudo make install
## Install is simple, you need to setup and properly configure alsa, then you can just build and run pocketsphinx
>       sudo apt-get update
>       sudo apt-get upgrade
>       cat /proc/asound/cards
* check your microphone is visible or not and if on which usb extension
>       sudo nano /etc/modprobe.d/alsa-base.conf
>       Now change this
>       Keep snd-usb-audio from being loaded as first soundsudcard
>       To options snd-usb-audio index=0
* if there is some other options snd-usb-audio index=1, comment it out
>       sudo reboot
>       cat /proc/asound/cards
* check your device is at 0
>       sudo apt-get install bison
>       sudo apt-get install libasound2-dev
* download sphinxbase latest, extract
>       ./configure --enable-fixed
>       make
>       sudo make install
* download pocketsphinx, extract
>       ./configure
>       make
>       sudo make install
>       export LD_LIBRARY_PATH=/usr/local/lib
>       export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
## Run it, should work
>       pocketsphinx_continuous -inmic yes

[tyler]: https://howchoo.com/u/tyler
