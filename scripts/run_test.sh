#!/bin/bash

# Main script for running throughput test

outfile="/tmp/foil_test.txt"

if [ -f $outfile ]
then
    rm $outfile
fi

# Create output file for printing
touch $outfile

# Is device connected?
./is_connected.sh > /dev/null
if [ $? -eq 1 ]
then
    echo Device not detected. >> $outfile
    exit 1
fi

# Start server in BG (save pid for the kill)
iperf -B 10.50.1.1 --server > /dev/null &
s_pid=$!

# Print CSV legend
echo timestamp,source_address,source_port,destination_address,\
destination_port,id,interval,transferred_bytes,bits_per_second >> $outfile

# Start client
# -t = time of tests (in seconds)
# -r = dual test (1 at a time)
iperf -B 10.50.0.1 -c 10.60.1.1 -t 15 -r --reportstyle C >> $outfile

# kill server (remove files? maybe that is a driver/GUI job)
kill -9 $s_pid
