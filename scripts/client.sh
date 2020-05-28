#!/bin/bash

# DON'T NEED THIS ANYMORE
# just added line into run_test.sh

# This script runs proper iperf command for client side of test
# we will edit this further to run the proper metrics

# -t = time of tests (in seconds)
# -i = pause n seconds inbetween periodic reports
# -r = dual test (1 at a time)
iperf -B 10.50.0.1 -c 10.60.1.1 -t 15 -r --reportstyle C
