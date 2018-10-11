# GKraken

![GKraken video](/art/gkraken-video.gif)

## Work in progress
The project is still in an early stage, use it at your own risk.

### TODO

- [x] Show fan and pump rpm
- [x] Show liquid temp in both app and app indicator
- [x] Show chart of selected profile
- [x] Show pump firmware version
- [x] Allow to select and apply a profile
- [x] Publish on PIP
- [x] Add option to restore last applyied profile on startup
- [x] Allow to hide main app window
- [x] Add command line option to start the app hidden
- [x] Add command line option to add/remove udev rule
- [ ] Add command line option to add/remove icon
- [ ] Edit Fixed speed profile
- [ ] Allow to select profiles from app indicator
- [ ] Add/Delete/Edit multi speed profiles
- [ ] About dialog
- [ ] Find better icons for app and app indicator
- [ ] Disable unsupported preferences
- [ ] Lighting
- [ ] Provide Ubuntu PPA

## How to install on (K/X)Ubuntu 18.04 or newer
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
#### Automatic way
Once GKraken is installed, the udev rule can be easily crated executing
```bash
sudo gkraken --udev-add-rule
```

#### Manual way
If for some reason the automatic way fails, you can always do if manually creating a new 
file in `/lib/udev/rules.d/60-gkraken.rules` containing this text:
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