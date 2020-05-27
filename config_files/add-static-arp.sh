#!/bin/bash

# This script will add static arp entries for FOIL test

iface_1="enp1s0"
iface_2="enp3s0"
mac_1="84:39:be:6d:29:89"
mac_2="84:39:be:6d:29:8A"

ip route add 10.60.1.1 dev $iface_1
arp -i $iface_1 -s 10.60.1.1 $mac_2 #enp3s0's mac address

ip route add 10.60.0.1 dev $iface_2
arp -i $iface_2 -s 10.60.0.1 $mac_1 #enp1s0's mac address
