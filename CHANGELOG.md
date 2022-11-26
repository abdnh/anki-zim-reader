# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2022-11-27

### Fixed

- Fix a critical error preventing the add-on from working in most situations (https://github.com/abdnh/anki-zim-reader/issues/16).

## [1.2.0] - 2022-11-23

### Added

- Add window to browse imported files.

## [1.1.0] - 2022-11-05

### Added

- Add support for Turkish Wiktionary.

### Changed

- Format example sentences as a list.

## [0.0.3] - 2022-10-18

### Added

- Allow customizing editor/browser shortcuts from the settings interface.
- Use [Libzim](https://github.com/openzim/libzim) on Linux and macOS to parse the ZIM files. This should work better than ZIMply.

### Changed

- Extract m/f/n gender abbreviations for the German parser instead of the full names.

### Fixed

- Fix issue with inflection table extraction for the Greek parser.
- Fix "internal server error" being shown for some missing words in the pop-up dictionary.

## [0.0.2] - 2022-10-08

### Added

- Support Anki versions 2.1.46>=,<=2.1.50
- Support image extraction for Greek and Spanish dictionaries.

### Fixed

- Fix images added by the add-on not being resized correctly using Anki's image resizer.

## [0.0.1] - 2022-10-06

Initial release.

[unreleased]: https://github.com/abdnh/anki-zim-reader/compare/1.2.0...HEAD
[1.2.0]: https://github.com/abdnh/anki-zim-reader/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/abdnh/anki-zim-reader/compare/1.0.0...1.1.0
[0.0.3]: https://github.com/abdnh/anki-zim-reader/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/abdnh/anki-zim-reader/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/abdnh/anki-zim-reader/commits/0.0.1
