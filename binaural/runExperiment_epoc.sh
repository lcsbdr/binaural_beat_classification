#!/bin/bash
python binauralExperiment.py -f out &
sleep 6
../emotiv/ozancaglayan/python-emotiv/examples/record-data.py 770 &
python shapecount.py
