#!/bin/bash
python3 setup.py sdist bdist_wheel
cd dist
latest=$(ls -Art | tail -n 1)
python3 -m pip install $latest
