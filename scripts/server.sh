#!/bin/bash

# This is script runs proper iperf command for server side of test
# ouptut as CSV --reportstyle c
# output as CSV --format M -> MBytes
iperf -B 10.50.1.1 -s 
