# ⚠ Project deprecated
This project is now deprecated in favor of [Coolero](https://gitlab.com/codifryed/coolero). If you are still using
GKraken, you are strongly advised to migrate to [Coolero](https://gitlab.com/codifryed/coolero).  
No new development is planned for GKraken and I do not own a Kraken device anymore, so I won't be able to provide 
even bug fixes.

# GKraken

<img src="/art/gkraken.png" width="128" align="right" hspace="0" />

GKraken is a GTK application that allows you to control the following AIO liquid coolers:

| Device | Pump | Fan | Lighting |
|:---|:---:|:---:|:---:|
| NZXT Kraken X40, X60, X31, X41, X51, X61 | :heavy_check_mark:<sup>_L_</sup> | :heavy_check_mark:<sup>_L_</sup>| :heavy_check_mark:<sup>_L_</sup> |
| NZXT Kraken X42, X52, X62, X72 | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| NZXT Kraken X53, X63, X73 | :white_check_mark: | :x: | :white_check_mark: |
| NZXT Kraken Z53, Z63, Z73 | :white_check_mark: | :white_check_mark: | :x: |

<sup>_L_</sup> _Limited functionality offered by legacy Kraken models_

## Table of contents

- [How to get GKraken](#-how-to-get-gkraken)
    - [Flathub](#install-from-flathub)
    - [Source](#install-from-source-code)
- [Running the App](#running-the-app)
    - [Adding Udev rule](#adding-udev-rule)
    - [Command line options](#command-line-options)
- [Building Flatpak](#-building-flatpak)
- [Running tests](#testing)
- [FAQ](#-faq)
- [How to help the project](#-how-to-help-the-project)
- [Acknowledgements](#-acknowledgements)
- [License](#license)

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

### Install from source code

#### Build time dependencies

| Distro                | pkg-config         | Python 3.6+ | gobject-introspection       | meson | ninja-build | appstream-util | libusb-1.0-0     | libudev       |
| --------------------- | ------------------ | ----------- | --------------------------- | ----- | ----------- | -------------- | ---------------- | ------------- |
| Arch Linux            | pkg-config         | python      | gobject-introspection       | meson | ninja       | appstream-glib | libusb           | libudev0      |
| Fedora                | pkgconf-pkg-config | python3     | gobject-introspection-devel | meson | ninja-build | appstream-util | libusbx-devel    | libudev-devel |
| Ubuntu                | pkg-config         | python3     | libgirepository1.0-dev      | meson | ninja-build | appstream-util | libusb-1.0-0-dev | libudev-dev   |

#### Run time dependencies

| Distro                | Python 3.6+ | pip         | gobject-introspection       | libappindicator          | gnome-shell-extension-appindicator |
| --------------------- | ----------- | ----------- | --------------------------- | ------------------------ | ---------------------------------- |
| Arch Linux            | python      | python-pip  | gobject-introspection       | libappindicator3         | gnome-shell-extension-appindicator |
| Fedora                | python3     | python3-pip | gobject-introspection-devel | libappindicator-gtk3     | gnome-shell-extension-appindicator |
| Ubuntu                | python3     | python3-pip | libgirepository1.0-dev      | gir1.2-appindicator3-0.1 | gnome-shell-extension-appindicator |

plus all the Python dependencies listed in [requirements.txt](requirements.txt)

#### Clone project and install

If you have not installed GKraken yet:

```bash
git clone --recurse-submodules -j4 https://gitlab.com/leinardi/gkraken.git
cd gkraken
git checkout release
sudo -H pip3 install -r requirements.txt
meson . build --prefix /usr
ninja -v -C build
sudo ninja -v -C build install
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
sudo -H pip3 install -r requirements.txt
meson . build --prefix /usr
ninja -v -C build
sudo ninja -v -C build install
```

#### Run

Once installed, to start it you can simply execute on a terminal:

```bash
gkraken
```

## Running the app

You can run the app from the desktop launcher or use the terminal:  
Run the command `gkraken` if installed from source, or if installed with flatpak `flatpak run com.leinardi.gkraken`.

The app needs to access the USB interface of the Kraken that, normally, is not available to unprivileged users.

To allow normal users to access the Kraken's USB interface you can create a custom udev rule

### Adding Udev rule

#### Using GKraken

Simply run:

```bash
gkraken --add-udev-rule
```

or with flatpak:

```bash
flatpak run com.leinardi.gkraken --add-udev-rule
```

It will automatically refresh also the udev rules. In some cases though, you may need to restart for the changes to take
effect

#### Manually

Create a new file in `/lib/udev/rules.d/60-gkraken.rules` containing this text:

```bash
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1e71", ATTRS{idProduct}=="170e", MODE="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1e71", ATTRS{idProduct}=="2007", MODE="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1e71", ATTRS{idProduct}=="3008", MODE="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="2433", ATTRS{idProduct}=="b200", MODE="0666"
```

After that, run the following commands

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=usb --attr-match=idVendor=1e71 --action=add
sudo udevadm trigger --subsystem-match=usb --attr-match=idVendor=2433 --action=add
```

## Command line options

| Parameter                 | Description                                                 | Source | Flatpak |
  |---------------------------|-------------------------------------------------------------|:------:|:-------:|
|-v, --version              |Show the app version                                         |    x   |    x    |
|--debug                    |Show debug messages                                          |    x   |    x    |
|--hide-window              |Start with the main window hidden                            |    x   |    x    |
|--add-udev-rule            |Add udev rule to allow execution without root permission     |    x   |    x    |
|--remove-udev-rule         |Remove udev rule that allow execution without root permission|    x   |    x    |
|--autostart-on             |Enable automatic start of the app on login                   |    x   |         |
|--autostart-off            |Disable automatic start of the app on login                  |    x   |         |

## 🖥 Building Flatpak

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

## Testing

To run the tests install the test dependencies:

```bash
pip install -r test-requirements.txt
```

and run from the project directory:

```bash
pytest
```

To check the Linters run from the project directory:

```bash
mypy gkraken
pylint gkraken
```

## ❓ FAQ

### The Flatpak version of GKraken is not using my theme, how can I fix it?

To fix this issue install a Gtk theme from Flathub. This way, Flatpak applications will automatically pick the installed
Gtk theme and use that instead of Adwaita.

Use this command to get a list of all the available Gtk themes on Flathub:

```bash
flatpak --user remote-ls flathub | grep org.gtk.Gtk3theme
```

And then just install your preferred theme. For example, to install Yaru:

```
flatpak install flathub org.gtk.Gtk3theme.Yaru
``````

### Where are the settings and profiles stored on the filesystem?

| Installation type |                     Location                     |
|-------------------|:------------------------------------------------:|
| Flatpak           |        `$HOME/.var/app/com.leinardi.gkraken/`        |
| Source code       | `$XDG_CONFIG_HOME` (usually `$HOME/.config/gkraken`) |

### ⚠ Dropped PyPI support

Production builds were previously distributed using PyPI. This way of distributing the software is simple but requires
the user to manually install all the non Python dependencies like cairo, glib, appindicator3, etc.  
A solution for all this problems is distributing the app via Flatpak, since with it all the dependencies will be bundled
and provided automatically, making possible to use new GTK features also on distributions using an older version of
Gnome.

**No new build will be published on PyPI**.

### Uninstall pip version

If you have already installed GKraken via `pip`, please make sure to uninstall it completely before moving to a newer
version:

```bash
pip3 uninstall gkraken
rm -rf ~/.config/gkraken
```

## 💚 How to help the project

### Discord server

If you want to help testing or developing it would be easier to get in touch using the Discord server of the
project: https://discord.gg/Q33n3UC  
Just write a message on the general channel saying how you want to help (test, dev, etc) and quoting @leinardi. If you
don't use discor but still want to help just open a new issue here.

### Can I support this project some other way?

Something simple that everyone can do is to star it on both [GitLab](https://gitlab.com/leinardi/gkraken)
and [GitHub](https://github.com/leinardi/gkraken). Feedback is always welcome: if you found a bug or would like to
suggest a feature, feel free to open an issue on the [issue tracker](https://gitlab.com/leinardi/gkraken/issues).

## ℹ️ Acknowledgements

Thanks to:

- Jonas Malaco for the [`liquidctl`](https://github.com/jonasmalacofilho/liquidctl) CLI library
- @codifryed for adding support of many new Kraken devices!

## License

```
This file is part of gkraken.

Copyright (c) 2021 Roberto Leinardi and Guy Boldon

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