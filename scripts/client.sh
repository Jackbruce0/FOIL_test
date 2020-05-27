#!/bin/bash

# This script runs proper iperf command for client side of test
# we will edit this further to run the proper metrics

# -t = time of tests (in seconds)
# -i = pause n seconds inbetween periodic reports
# -d = dual test
# -r = dual test (1 at a time)

iperf -B 10.50.0.1 -c 10.60.1.1 -t 45 -i 10 -r
