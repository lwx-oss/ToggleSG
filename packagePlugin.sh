#!/bin/bash


if [ -f "toggleSG.zip" ]; then
    rm "toggleSG.zip"
fi

zip -r -0 toggleSG.zip plugin.togglesg.lwx
