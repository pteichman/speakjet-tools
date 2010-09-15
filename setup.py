#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "speakjet-tools",
    version = "0.1",
    author = "Peter Teichman",
    author_email = "peter@teichman.org",
    url = "http://wiki.github.com/pteichman/speakjet-tools/",
    description = "Tools for precomputing SpeakJet voice synth commands",
    packages = ["speakjet"],
    test_suite = "tests",
    install_requires = ["argparse>=1.1"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    entry_points = {
        "console_scripts" : [
            "speakjet = speakjet.control:main"
        ]
    }
)
