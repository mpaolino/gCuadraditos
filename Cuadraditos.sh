#!/bin/sh
CURRENT_DIR=`pwd`
export LD_LIBRARY_PATH="$CURRENT_DIR/lib"
export GST_PLUGIN_PATH="$CURRENT_DIR/lib"

python gCuadraditos.py

