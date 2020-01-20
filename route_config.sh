#!/bin/bash

# RUN THIS SCRIPT AS ROOT 

# this script will force loopback traffic through ethernet ports (given ip's arent changed)
# enp1s0 = 10.50.0.1
# enp3s0 = 10.50.1.1

# nat source IP 10.50.0.1 -> 10.60.0.1 when going to 10.60.1.1
iptables -t nat -A POSTROUTING -s 10.50.0.1 -d 10.60.1.1 -j SNAT --to-source 10.60.0.1

# nat inbound 10.60.0.1 -> 10.50.0.1
iptables -t nat -A PREROUTING -d 10.60.0.1 -j DNAT --to-destination 10.50.0.1

# nat source IP 10.50.1.1 -> 10.60.1.1 when going to 10.60.0.1
iptables -t nat -A POSTROUTING -s 10.50.1.1 -d 10.60.0.1 -j SNAT --to-source 10.60.1.1

# nat inbound 10.60.1.1 -> 10.50.1.1
iptables -t nat -A PREROUTING -d 10.60.1.1 -j DNAT --to-destination 10.50.1.1


# Now tell the system how to get to each fake network, and prepopulate the arp entries
ip route add 10.60.1.1 dev enp1s0
arp -i enp1s0 -s 10.60.1.1 40:62:31:08:4F:A4 #enp3s0's mac address

ip route add 10.60.0.1 dev enp3s0
arp -i enp3s0 -s 10.60.0.1 40:62:31:08:4F:A3 #enp1s0's mac address


