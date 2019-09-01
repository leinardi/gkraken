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

## 📦 How to get GKraken
### Install from Flathub
This is the preferred way to get GKraken on any major distribution (Arch, Fedora, Linux Mint, openSUSE, Ubuntu, etc).

If you don't have Flatpak installed you can find step by step instructions [here](https://flatpak.org/setup/).

Make sure to have the Flathub remote added to the current user:

```bash
flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

#### Install
```bash
flatpak --user install flathub com.leinardi.gkraken
```

#### Run
```bash
flatpak run com.leinardi.gkraken
```

### Distro specific packages
### Install from source code
#### Dependencies for (K/X)Ubuntu 18.10 or newer
```bash
sudo apt install git meson python3-pip libcairo2-dev libgirepository1.0-dev libglib2.0-dev libdazzle-1.0-dev gir1.2-gtksource-3.0 gir1.2-appindicator3-0.1 python3-gi-cairo appstream-util
```

#### Dependencies for Fedora 28 or newer
```bash
dnf install desktop-file-utils git gobject-introspection-devel gtk3-devel libappstream-glib libdazzle libnotify meson python3-cairocffi python3-devel python3-pip redhat-rpm-config
```

#### Clone project and install
If you have not installed GKraken yet:
```bash
git clone --recurse-submodules -j4 https://gitlab.com/leinardi/gkraken.git
cd gkraken
git checkout release
pip3 install -r requirements.txt
meson . build --prefix /usr
ninja -v -C build
ninja -v -C build install
```

#### Update old installation
If you installed GKraken from source code previously and you want to update it:
```bash
cd gkraken
git fetch
git checkout release
git reset --hard origin/release
git submodule init
git submodule update
pip3 install -r requirements.txt
meson . build --prefix /usr
ninja -v -C build
ninja -v -C build install
```

#### Run
Once installed, to start it you can simply execute on a terminal:
```bash
gkraken
```

## Running the app
To start the app you have to run the command `gkraken` in a terminal. The app needs to access the USB interface of the Kranen that, normally,
is not available to unprivileged users. 

To allow normal users to access the Kraken's USB interface you can 
create a custom udev rule

### Udev rule
Simply create a new file in `/lib/udev/rules.d/60-gkraken.rules` containing this text:
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

  | Parameter                 | Description                                                 | Source | Flatpak |
  |---------------------------|-------------------------------------------------------------|:------:|:-------:|
  |-v, --version              |Show the app version                                         |    x   |    x    |
  |--debug                    |Show debug messages                                          |    x   |    x    |
  |--hide-window              |Start with the main window hidden                            |    x   |    x    |
  |--application-entry        |Add a desktop entry for the application                      |    x   |         |
  |--autostart-on             |Enable automatic start of the app on login                   |    x   |         |
  |--autostart-off            |Disable automatic start of the app on login                  |    x   |         |
  |--udev-add-rule            |Add udev rule to allow execution without root permission     |    x   |         |
  |--udev-remove-rule         |Remove udev rule that allow execution without root permission|    x   |         |


## 🖥️ Build, install and run with Flatpak
If you don't have Flatpak installed you can find step by step instructions [here](https://flatpak.org/setup/).

Make sure to have the Flathub remote added to the current user:

```bash
flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Clone the repo
```bash
git clone --recurse-submodules -j4 https://gitlab.com/leinardi/gkraken.git
```
It is possible to build the local source or the remote one (the same that Flathub uses)
### Local repository
```bash
./build.sh --flatpak-local --flatpak-install
```
### Remote repository
```bash
./build.sh --flatpak-remote --flatpak-install
```
### Run
```bash
flatpak run com.leinardi.gkraken --debug
```

## 🖥️ How to build and run the source code
If you want to clone the project and run directly from the source you need to manually install all the needed
dependencies.
 
### (K/X)Ubuntu 18.04 or newer
See [Install from source](https://gitlab.com/leinardi/gkraken#kxubuntu-1810-or-newer-dependencies)

### Fedora 28+ (outdated, please let me know if new dependencies are needed)
Install [(K)StatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/)

### Python dependencies
```bash
git clone --recurse-submodules -j4 https://gitlab.com/leinardi/gkraken.git
cd gkraken
pip3 install -r requirements.txt
```

### Build and Run
```bash
./run.sh
```

## ❓ FAQ
### The Flatpak version of GKraken is not using my theme, how can I fix it?
Due to sandboxing, Flatpak applications use the default Gnome theme (Adwaita), 
and not whatever Gtk theme you're currently using.  
The fix for this issue is to install your current Gtk theme from Flathub. 
This way, Flatpak applications will automatically pick the installed Gtk theme 
and use that instead of Adwaita.

Use this command to get a list of all the available Gtk themes on Flathub:
```bash
flatpak --user remote-ls flathub | grep org.gtk.Gtk3theme
```
And then just install your preferred theme. For example, to install Yaru:
```
flatpak install flathub org.gtk.Gtk3theme.Yaru
```

### Where are the settings and profiles stored on the filesystem?
| Installation type |                     Location                     |
|-------------------|:------------------------------------------------:|
| Flatpak           |        `$HOME/.var/app/com.leinardi.gkraken/`        |
| Source code       | `$XDG_CONFIG_HOME` (usually `$HOME/.config/gkraken`) |

## 💚 How to help the project

### Discord server
If you want to help testing or developing it would be easier to get in touch using the discord server of the project: https://discord.gg/YjPdNff  
Just write a message on the general channel saying how you want to help (test, dev, etc) and quoting @leinardi. If you don't use discor but still want to help just open a new issue here.


### Can I support this project some other way?

Something simple that everyone can do is to star it on both [GitLab](https://gitlab.com/leinardi/gkraken) and [GitHub](https://github.com/leinardi/gkraken).
Feedback is always welcome: if you found a bug or would like to suggest a feature,
feel free to open an issue on the [issue tracker](https://gitlab.com/leinardi/gkraken/issues).

## ⚠ Dropped PyPI support
Development builds were previously distributed using PyPI. This way of distributing the software is simple
but requires the user to manually install all the non Python dependencies like cairo, glib, appindicator3, etc.  
The current implementation of the historical data uses a new library, Dazzle, that requires Gnome 3.30 which is
available, using Python Object introspection, only starting from Ubuntu 18.10 making the latest Ubuntu LTS, 18.04,
unsupported.    
A solution for all this problems is distributing the app via Flatpak, since with it all the dependencies
will be bundled and provided automatically, making possible to use Gnome 3.30 features also on distributions
using an older version of Gnome.

**No new build will be published on PyPI**.

### Uninstall pip version
If you have already installed GKraken via `pip`, please make sure to uninstall it completely before moving to a newer version:

```bash
pip3 uninstall gkraken
rm -rf ~/.config/gkraken
```

## ℹ️ Acknowledgements
Thanks to:

 - Jonas Malaco for the [`liquidctl`](https://github.com/jonasmalacofilho/liquidctl) CLI library

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