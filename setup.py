import os

from setuptools import setup


def read(fname: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


setup(
    name="zim_reader",
    version="1.2.1",
    description="ZIM file reader for Anki",
    long_description=read("README.md"),
    author="Abdo",
    author_email="abd.nh25@gmail.com",
    url="https://github.com/abdnh/anki-zim-reader",
    package_dir={"zim_reader": "src"},
    packages=["zim_reader", "zim_reader.dictionaries"],
    keywords="anki addon zim dictionary",
    install_requires=[
        "anki>=2.1.46",
        "aqt>=2.1.46",
    ],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
