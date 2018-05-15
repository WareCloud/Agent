## Overview

WareCloud: Agent (0.1) Beta

## Requirements

+ Python: 3.7
+ Platform: Linux, Windows
+ WMI ≥ 1.0+ /// Windows Only
+ parse ≥ 1.8+
+ psutil ≥ 5.3.0+

## Install requirements
pip install -r requirements.txt

## Run

python server.py --ssl 0 --cert ./cert.pem

or

python server.py

## Create .exe

rm -rf build
python setup.py build

## Run .exe

Agent/build/exe.win32-3.6/server.exe

