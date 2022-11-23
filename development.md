## Contributing

Any kind of contributions are welcome, especially for adding support for more dictionaries or improving existing ones.
Extracting information from the ZIM files involves parsing the HTML content.
See [`greek.py`](./src/dictionaries/greek.py) for an example of how it's done for Greek. After you add a new file for your language under the [`dictionaries`](./src/dictionaries/) subfolder, simply add the class name to the parsers list in [`dictionaries/__init__.py`](src/dictionaries/__init__.py) and you're good to go!

## Building the add-on

The add-on is packaged using a [Makefile](./Makefile). To build the add-on and test your changes:

1. Install requirements: `pip install -r requirements.txt`.
2. Run `make zip` to produce `build/zim_reader.ankiaddon`. This will also generate the PyQt forms under [src/forms](./src/forms/).
3. You can then either extract the zip to your add-ons folder or symlink the src folder.

If you want to contribute some changes, also making sure to do the following is appreciated:

1. Run `make check` to check for various lint warnings.
2. Fix any formatting issues automatically using `make fix`.
3. Fix any Mypy and Pylint errors caused by your changes manually.

## Accessing from other add-ons

The add-on was written with the intention to provide other add-ons access to its functionality in mind.
See how this is done in my fork of the [Create subs2srs cards with mpv](https://github.com/abdnh/create-subs2srs-cards-with-mpv-video-player/tree/intersubs) add-on.

TODO: document the interface.
