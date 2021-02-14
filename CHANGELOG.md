Version 1.0.0
=============
Released: 2021-02-14

 * Fixed #21 and #31: Added 4th gen device support! Huge thanks to @codifryed
   for this code contribution
 * Updated dependencies

Version 0.14.5
==============
Released: 2020-12-09

 * Project in maintenance mode!
 * Gracefully handle locale.{bind,}textdomain not being available (thanks
   @Cogitri)

Version 0.14.4
==============
Released: 2020-06-28

 * Disabled check for new App version on launch (it's now opt-in)
 * Updated dependencies

Version 0.14.3
==============
Released: 2020-05-17

 * Improved text of UDEV rules dialogs

Version 0.14.2
==============
Released: 2020-05-17

 * Added dialog suggesting possible fix for UDEV rules

Version 0.14.1
==============
Released: 2020-04-09

 * Updated dependencies

Version 0.14.0
==============
Released: 2019-09-29

 * Updated several dependencies, including liquidctl 1.3.3
 * Added support for 50% pump duty on latest firmware versions
 * Added warning dialog for legacy firmware 2.x

Version 0.13.0
==============
Released: 2019-09-26

 * Using Flatpak and Flathub to distribute the application
 * Using meson as build system
 * Give option to minimize to tray when closing from the X button
 * Quit App with Ctrl+Q and hide it with Ctrl+H
 * Renamed parameters `udev-add-rule` and `udev-remove-rule` to `add-udev-rule`
   and `remove-udev-rule`
 * Several library updates

Version 0.12.1
==============
Released: 2018-10-20

 * Set dialogs "transient for" property

Version 0.12.0
==============
Released: 2018-10-20

 * Added option to launch the App hidden on login
 * Added command line option to add desktop entry
 * Synced App and indicator menus
 * Added missing dependencies to PyPI
 * Some code refactoring

Version 0.11.0
==============
Released: 2018-10-14

 * Added check for new versions
 * Added Add/Edit/Delete of multi speed profiles
 * Small icon change

Version 0.10.0
==============
Released: 2018-10-12

 * Added about dialog
 * Added better App and App indicator icons

Version 0.9.0
=============
Released: 2018-10-12

 * Added ability to edit Fixed speed profile
 * Added command line options (run `gkraken -h` for more info)
 * Added command line option to start the App hidden
 * Added command line option to add/remove udev rule
 * Load last applied profile enabled by default

Version 0.8.0
=============
Released: 2018-10-09

 * Improved fan and pump charts
 * Better driver error handling

Version 0.7.0
=============
Released: 2018-10-09

 * Added ability to load last applied profile on App start
 * Added App indicator with water temp
