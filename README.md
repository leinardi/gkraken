# GKraken
GKraken is a GTK application that allows you to control the cooling
(and soon also the lighting) of a NZXT Kraken X (X42, X52, X62 or X72) 
pump from Linux.

## TODO
<img src="/art/gkraken.png" width="256" align="right" hspace="0" />

- [x] Show fan and pump rpm
- [x] Show liquid temp in both app and app indicator
- [x] Show chart of selected profile
- [x] Show pump firmware version
- [x] Allow to select and apply a profile
- [x] Publish on PIP
- [x] Add option to restore last applied profile on startup
- [x] Allow to hide main app window
- [x] Add command line option to start the app hidden
- [x] Add command line option to add/remove udev rule
- [x] Add Refresh timeout to settings 
- [x] Add command line option to add desktop entry
- [x] Edit Fixed speed profile
- [ ] Allow to select profiles from app indicator
- [x] Add/Delete/Edit multi speed profiles
- [x] About dialog
- [x] Find better icons for app and app indicator
- [ ] Disable unsupported preferences
- [ ] Lighting
- [ ] Provide Ubuntu PPA
- [ ] Add support for i18n (internationalization and localization)

## Screenshots
<img src="/art/screenshot-09.png" width="844"/>

<img src="/art/screenshot-08.png" width="844"/>

<img src="/art/screenshot-05.png" width="844"/>

## Video
Click [here](https://gitlab.com/leinardi/gkraken/blob/master/art/video.mp4) to see a short video of the application.

## Distribution dependencies
### (K/X)Ubuntu 18.04 or newer
```bash
sudo apt install gir1.2-gtksource-3.0 gir1.2-appindicator3-0.1 python3-gi-cairo python3-pip
```
### Fedora 28+
Install [(K)StatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/)

### Arch Linux (Gnome)
```bash
sudo pacman -Syu python-pip libappindicator-gtk3
```

## Install using PIP
```bash
pip3 install gkraken
```
Add the the executable path `~/.local/bin` to your PATH variable if missing.

## Update using PIP
```bash
pip3 install -U gkraken
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
sudo `which gkraken` --udev-add-rule
```

### Application entry
To add a desktop entry for the application run the following command:
```bash
gkraken --application-entry 
```

#### Manual way
If for some reason the automatic way fails, you can always do it manually by creating a new 
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

## Command line options

  | Parameter                 | Description|
  |---------------------------|------------|
  |-v, --version              |Show the app version|
  |--debug                    |Show debug messages|
  |--hide-window              |Start with the main window hidden|
  |--application-entry        |Add a desktop entry for the application|
  |--autostart-on             |Enable automatic start of the app on login|
  |--autostart-off            |Disable automatic start of the app on login|
  |--udev-add-rule            |Add udev rule to allow execution without root permission|
  |--udev-remove-rule         |Remove udev rule that allow execution without root permission|



## Python dependencies
## How to run the repository sources

```
sudo apt install python3-pip
git clone https://gitlab.com/leinardi/gkraken.git
cd gkraken
pip3 install -r requirements.txt
./run
```

## How can I support this project?

The best way to support this plugin is to star it on both [GitLab](https://gitlab.com/leinardi/gkraken) and [GitHub](https://github.com/leinardi/gkraken).
Feedback is always welcome: if you found a bug or would like to suggest a feature,
feel free to open an issue on the [issue tracker](https://gitlab.com/leinardi/gkraken/issues).

## License
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