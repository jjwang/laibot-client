# Sound card issues of RPi（树莓派声卡问题大全）

## PocketSphinx 的树莓派声卡问题

    cat /proc/asound/cards
check your microphone is visible or not and if on which usb extension

    sudo nano /etc/modprobe.d/alsa-base.conf
Now change this

    Keep snd-usb-audio from being loaded as first soundcard 
    options snd-usb-audio index=-2
To

    Keep snd-usb-audio from being loaded as first soundcard 
    options snd-usb-audio index=0
if there is some other options snd-usb-audio index=1 , make it as comment

    sudo reboot 
    cat /proc/asound/cards 
check your device is at 0

    sudo apt-get install bison
    sudo apt-get install libasound2-dev
download sphinxbase latest , extract

    ./configure --enable-fixed
    make
    sudo make install
download pocketsphinx, extract

    ./configure
    make
    sudo make install
    export LD_LIBRARY_PATH=/usr/local/lib 
    export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
go to src/programs/

    pocketsphinx_continuous -samprate 16000/8000/48000
Cheers :)
