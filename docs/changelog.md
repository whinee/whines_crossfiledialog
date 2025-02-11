# Changelog

## 1.0.0

Initial Release of the package. Notable changes from the [original Github repository](https://github.com/maikelwever/crossfiledialog) include the following:

### Added

- GTK (via PyGObject) and Qt5/6 (via pyqt5/pyqt6) support.
- Sophisticated filter processor so that filter processing is consistent among file pickers across different platforms.
- Ability to pick at which order the file pickers are tested and picked in Linux.
- Documentation on how to develop the app in different platforms, such as how to install the dependencies required for developing this library
- Comtypes for folder picking in Windows so that the folder picker follows the dark mode theme of the OS whenever it is turned on.

### Fixed

- Linted and fixed warnings
