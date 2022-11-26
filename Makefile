.PHONY: all zip clean check check_format fix mypy pylint ankiweb test vendor serve

all: zip

zip:
	python -m ankibuild --type package --qt all --noconsts --forms-dir forms --exclude user_files/**/ $(EXTRA_ARGS)

ankiweb:
	python -m ankibuild --type ankiweb --qt all --noconsts --forms-dir forms --exclude user_files/**/ $(EXTRA_ARGS)

check: check_format mypy pylint

check_format:
	python -m black --exclude="forms|ankidata|samples|user_files|vendor" --check --diff --color src tests
	python -m isort --check --diff --color src tests

fix:
	python -m black --exclude="forms|ankidata|samples|user_files|vendor" src tests
	python -m isort src tests

mypy:
	python -m mypy src tests

pylint:
	python -m pylint src tests

samples/%.zim:
	mkdir -p samples
	curl -L https://download.kiwix.org/zim/$(notdir $@) -o $@

# TODO: download other supported files
download-test-data: samples/wiktionary_el_all_maxi.zim

test: download-test-data
	python -m pytest tests

PY_VER := 39

vendor:
	./scripts/vendor_no_platform.sh
	./scripts/vendor_pyzstd.sh $(PY_VER)
	./scripts/vendor_libzim.sh $(PY_VER)

serve:
	python -m src $(FILE)

clean:
	rm -rf build/
