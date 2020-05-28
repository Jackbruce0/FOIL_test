#!/bin/bash

# Checks if there is a link between enp1s0 and enp3s0
# 10.60.0.1 is the address in nat table for reaching adapter "over the wire"

# 0 -> connected
# 1 -> not connected

ping 10.60.0.1 -c 1 -W 1 > /dev/null

if [ $? -eq 0 ]
then
    echo Device is connected
    exit 0
else
    echo Device is not connected
    exit 1
fi
