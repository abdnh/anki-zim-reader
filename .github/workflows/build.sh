#!/bin/bash

pip install git+https://github.com/abdnh/ankibuild@6d5f33d5fb781cf889eb982b9999a5b2f2608659#egg=ankibuild[qt5,qt6]
make vendor
make
