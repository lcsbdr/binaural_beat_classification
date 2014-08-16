#!/bin/bash
../emotiv/ozancaglayan/python-emotiv/examples/record-data.py 135 &
python captureEEGEye_Emotiv.py --folder captures
