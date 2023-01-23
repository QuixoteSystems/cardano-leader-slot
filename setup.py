#!/usr/bin/env python3

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    version = '1.0.0',
    name = 'Cardano Leader Slot',
    author = 'Quixote Stake Pool',
    author_email = 'quixotepool@proton.me',
    url = 'https://github.com/QuixoteSystems',
    license = 'MIT',
    description = 'Scheduled Block Checker for Cardano Stakepool Operators.',
    long_description= LONG_DESCRIPTION,
    long_description_content_type= 'text/markdown',
    keywords = ['koios', 'blockchain', 'cardano', 'SPO', 'Pool Tool', 'python'],
    include_package_data = True,
    packages = find_packages(include=['cardano-leaderslot']),
    install_requieres = ["requests", "urllib3", "readchar", "pyfiglet", "koios-python", "tzlocal"],
    dependency_links=["git+ssh://git@github.com:cardano-community/koios-python.git"],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: SPOs',

        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
)