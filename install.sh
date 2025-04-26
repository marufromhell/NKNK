#!/bin/bash
python -m venv ~/venv/
chmod u+x nk.py
sudo cp ./nksh /usr/bin
sudo chmod u+x /usr/bin/nksh
sudo dnf install xonsh
~/venv/bin/pip install -r requirements.txt
