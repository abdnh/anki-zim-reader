## Contributing

Any kind of contributions are welcome, especially for adding support for more dictionaries or improving existing ones.
Extracting information from the ZIM files involves parsing the HTML content.
See [`greek.py`](./src/dictionaries/greek.py) for an example of how it's done for Greek. After you add a new file for your language under the [`dictionaries`](./src/dictionaries/) subfolder, simply add the class name to the parsers list in [`dictionaries/__init__.py`](src/dictionaries/__init__.py) and you're good to go!

## Building the add-on

The add-on is packaged using a [Makefile](./Makefile). To build the add-on and test your changes:

1. Install requirements: `pip install -r requirements.txt`.
2. Run `make zip` to produce `build/zim_reader.ankiaddon`. This will also generate the PyQt forms under [src/forms](./src/forms/).
3. You can then either extract the zip to your add-ons folder or symlink the src folder.

Alternatively, you can get bleeding-edge build of the add-on from the [Actions](https://github.com/abdnh/anki-zim-reader/actions?query=is%3Asuccess+event%3Apush+branch%3Amaster++) tab. Click the topmost commit with a green checkmark, then click "builds" in the Artifacts section. You'll get a zip that contains *multiple zip/ankiaddon files* for the different Anki versions we support.

If you want to contribute some changes, also making sure to do the following is appreciated:

1. Run `make check` to check for various lint warnings.
2. Fix any formatting issues automatically using `make fix`.
3. Fix any Mypy and Pylint errors caused by your changes manually.
