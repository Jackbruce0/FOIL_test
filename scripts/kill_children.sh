#!/bin/bash

# Script that gets pids of child processes from run_test.sh
# this is definitely not the best way to do this :)

# Command -> pid of iperf
kill -9 $(ps auxww | grep iperf | grep reportstyle | awk '{print $2}')
kill -9 $(ps auxww | grep iperf | grep server | awk '{print $2}')

exit 0
