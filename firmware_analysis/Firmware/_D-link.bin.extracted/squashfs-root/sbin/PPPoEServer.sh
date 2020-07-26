#!/bin/sh
# Copyright (C) 2006 OpenWrt.org

ACTION=$1
if [ $ACTION = "start" ]; then
	echo 1 > /proc/sys/net/ipv4/ip_forward
	ipaddr=`uci get network.lan.ipaddr`
	/usr/sbin/pppoe-server -T 60 -I br-lan -N 100 -L $ipaddr -R 192.168.0.100
elif [ $ACTION = "stop" ]; then
	killall pppoe-server
fi	
