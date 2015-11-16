# pi-spectrometer
## Installation
### From Raspbian image
The following instructions describe how to install pi-sepctrometer on a fresh Raspbian image.

1. Download the latest Raspbian image from the raspberry pi website (https://www.raspberrypi.org/downloads/raspbian/)
2. Unzip the downloaded file
3. Write the image to an SD card (https://www.raspberrypi.org/documentation/installation/installing-images/)
4. Insert the SD card into the Raspberry Pi
5. Insert a monitor, keyboard and mouse into the Raspberry Pi
6. Insert a Wifi Dongle into the Raspberry Pi
7. Power on the Raspberry Pi
8. Wait for the Desktop to appear
9. Connect to a Wifi network by clicking on the networking icon on the top right.
10. Click on the terminal icon on the top panel.
11. `cd` into a suitable directory to install the Pi Spectrometer
12. Type `git clone https://github.com/IonSystems/pi-spectrometer.git`
13. Type `sudo apt-get install python-opencv`
14. Type `sudo apt-get install python-imaging-tk`
15. Type `sudo apt-get install python-matplotlib`
16. Type `sudo raspi-config` and enable the Raspberry Pi Camera.

