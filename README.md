<img src="./src/icons/logo.svg" width="250">

**Work in progress**

Anki add-on that allows you to import [ZIM](<https://en.wikipedia.org/wiki/ZIM_(file_format)>) files
and access their data inside Anki. The main focus of the add-on is to support extracting information such word definitions, example sentences, pronunciation, etc. from the Wiktionary ZIM files and add them to notes.

This is a fork of the [Wiktionary](https://github.com/abdnh/anki-wiktionary) add-on. The plan was to add ZIM support to the Wiktionary add-on in addition to the original support for Kaikki files, but I got some ideas to extend the add-on with ZIM-specific additions like a pop-up dictionary and a local server that can be accessed from other add-ons, so I decided to split it into a new add-on to keep the Wiktionary add-on simple.

## Supported dictionaries

Currently supported dictionaries are the Greek and the Spanish Wiktionary files.[^1]
Pull requests to add support for more dictionaries and improve existing ones are very much appreciated. The HTML content of the entries stored in the ZIM file needs to be parsed for that. See [greek.py](./src/dictionaries/greek.py) for an example of how it's done for Greek.
If you want to see support for your language, you can open a feature request in the [issue tracker](https://github.com/abdnh/anki-zim-reader/issues).

## Usage

### Importing a ZIM file

The dialog under _Tools > ZIM Reader > Import a file_ allows you to import a new ZIM file and make it available for use in the add-on. [This page](https://wiki.kiwix.org/wiki/Content_in_all_languages) has a lot of ZIM files available for download.

<img src="./images/import_dialog.png" width="600">

### Filling in notes

The add-on provides an interface to fill existing notes with defintions, example sentences, etc. from imported files.
The interface can either be accessed from a button in the editor, or via the _Edit > Bulk-define from ZIM file_ menu
item in the browser for bulk operations on selected notes. You can also configure shortcuts from _Tools > Add-ons_.

<img src="./images/dialog.png" width="600">

Explanation of some options:

- **File**: The imported ZIM file you want to extract info from.
- **Parser**: For the add-on to understand how to extract data from the chosen file, you need to tell it what "parser" it should use to do that. Only a limited number of ZIM files for a couple of languages currently have parsers.
- **Word**: The field where the word you want to query exists.
- The other options decide to which field each kind of supported info goes.

### Pop-up dictionary

There is also a feature to look up words in the reviewing screen in imported ZIM files.
Unlike the "fill-in" feature, this should work on any imported ZIM file without the need for a special parser.
If you select any word and press "Alt+Shift+S", a pop-up should be shown with the page of the selected word if found.
You can configure the ZIM file used for the pop-up feature and some other settings from the [Settings](#settings) dialog.

<img src="./images/popup.png" width="600">

### Settings

You can configure some settings of the add-on from _Tools > ZIM Reader > Settings_.
Currently only the pop-up dictionary's settings are configurable here.
For the parser option, if your chosen dictionary file doesn't have a dedicated parser, you can simply choose the "Default" parser. Parsers here are currently only useful to convert a word to its base form and search for that instead using language-specific rules if the exact word doesn't have a page in the dictionary.

<img src="./images/settings.png" width="600">

## Download

TODO: publish to AnkiWeb

## TODO

Currently planned features are

- [x] A pop-up feature that can be used to look up any word on the reviewer in imported ZIM files and view them in a nice format like in [Kiwix](https://www.kiwix.org/).
- [ ] An API to allow other add-ons to make use of the add-on's features. Specifically, I plan to extend the [Create subs2srs cards with mpv video player](https://ankiweb.net/shared/info/1213145732) with a pop-up dictionary inside mpv with the support of [intersubs](https://github.com/abdnh/intersubs).
- [ ] Change shortcuts to avoid conflicts with Wiktionary
- [ ] Update ankiweb_page.html and publish add-on

## License

GPLv3 or later. See [LICENSE](./LICENSE).

## Credit

- The logo is adapted from the [Kiwix logo](https://en.wikipedia.org/wiki/File:Kiwix_logo_v3.svg) (licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en)) and the Anki logo from the [Papirus icon theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme) (licensed under the [GPLv3](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme/blob/master/LICENSE)).
- The [zimply-core](https://github.com/dylanmccall/zimply-core) library is used to extract data from ZIM files. See [license](https://github.com/dylanmccall/zimply-core/blob/master/LICENSE.txt).

## Support me

Consider supporting me on Ko-fi or Patreon if you like my add-ons:

<a href='https://ko-fi.com/U7U8AE997'><img height='36' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a> <a href="https://www.patreon.com/abdnh"><img height='36' src="https://i.imgur.com/mZBGpZ1.png"></a>

I'm also available for freelance add-on development at Fiverr:

<a href="https://www.fiverr.com/abd_nh/develop-an-anki-addon"><img height='36' src="https://i.imgur.com/0meG4dk.png"></a>

[^1]: Specifically, the "wiktionary (Ελληνικά)" and "wiktionary (español)" dictionaries in https://wiki.kiwix.org/wiki/Content_in_all_languages
