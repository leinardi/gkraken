# GKraken

![GKraken video](/art/gkraken-video.gif)

## Work in progress
The project is still in an early stage, use it at your own risk.

## How to install on (K)Ubuntu 18.10
```bash
# install dependencies
sudo apt install gir1.2-gtksource-3.0 gir1.2-appindicator3-0.1 python3-gi-cairo python3-pip
# install gkraken
sudo pip3 install gkraken
```

## Running the app
To start the app you have to run the command `gkraken` in a terminal. The app needs to access the USB interface of the Kranen that, normally,
is not available to unprivileged users. 

To allow normal users to access the Kraken's USB interface you can 
create a custom udev rule

### Udev rule
Create a new file `/lib/udev/rules.d/60-gkraken.rules` and add inside this text:
```bash
SUBSYSTEM=="usb", ATTRS{idVendor}=="1e71", ATTRS{idProduct}=="170e", MODE="0666"
```

After that, run the following commands
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=usb --attr-match=idVendor=1e71 --action=add
```

If you don't want to create this custom rule you can run gkraken as root 
(using sudo) but we advise against this solution.


## Python dependencies
### PIP
* injector
* liquidctl
* matplotlib
* peewee
* pyxdg
* rx

## How to compile it on Ubuntu 18.04

```
sudo apt install python3-pip
git clone https://gitlab.com/leinardi/gkraken.git
pip3 install injector
pip3 install liquidctl
pip3 install matplotlib
pip3 install peewee
pip3 install pyxdg
pip3 install rx
ca gkraken
./gkraken.py
```

## Lincense
```
This file is part of gkraken.

Copyright (c) 2018 Roberto Leinardi

gkraken is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gkraken is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gkraken.  If not, see <http://www.gnu.org/licenses/>.
```