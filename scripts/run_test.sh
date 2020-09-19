#!/bin/bash

# Main script for running throughput test

#shutdown() {
## Get our prrocess group id
#    echo shutdown initiatedd!!!
#    PGID=$(ps -o pgid= $$ | grep -o [0-9]*)
#
#    echo shutdown initiatedd!!!
#    # Kill it in a new processs group
#    setsid kill -- -$PGID
#    echo shutdown initiatedd!!!
#    exit 0
#}

script_dir="/home/djm/FOIL_test/scripts/"
outfile="/tmp/foil_test.txt"


#trap "shutdown" SIGINT SIGTERM SIGKILL

if [ -f $outfile ]
then
    rm $outfile
fi

# Create output file for printing
touch $outfile

# Is device connected?
${script_dir}is_connected.sh > /dev/null
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
iperf -B 10.50.0.1 -c 10.60.1.1 -t 10 -r --reportstyle C >> $outfile

# kill server (remove files? maybe that is a driver/GUI job)
kill -9 $s_pid

