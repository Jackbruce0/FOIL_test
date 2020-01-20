#!/bin/bash

# This script runs proper iperf command for client side of test
# we will edit this further to run the proper metrics

iperf -B 10.50.0.1 -c 10.60.1.1 -t 60 -i 10
