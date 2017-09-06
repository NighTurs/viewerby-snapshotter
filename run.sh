#!/usr/bin/env bash

source env/bin/activate
nohup python3 snapshotter.py --clients 126 127 &
