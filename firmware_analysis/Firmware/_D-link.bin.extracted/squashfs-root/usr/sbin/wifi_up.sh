#!/bin/sh
#
#wifi_down.sh
#
#useing:crond for wifi down
#

ntp_flag=`cat /var/ntpd_sync`
network_mode=`uci get network.globals.network_mode`

if [ "$ntp_flag" = "1" ]; then
	ra24=`iwconfig ra0 | grep ESSID`
	ra5=`iwconfig rai0 | grep ESSID`
	ra24_disable=`uci get wireless.@wifi-iface[3].disabled`
	ra5_disable=`uci get wireless.@wifi-iface[0].disabled`

	if [ ${network_mode} = "repeater" ]; then
		if [ "$ra24_disable" = "0" ]; then
			ifconfig ra0 up
		fi
		
		if [ "$ra5_disable" = "0" ]; then
			ifconfig rai0 up
		fi	

	else
		if [ -z "$ra24" -a -z "$ra5" ]; then
			wifi up
		elif [ -z "$ra24" -a "$ra24_disable" = "0" ]; then
			ifconfig ra0 up
		elif [ -z "$ra5" -a "$ra5_disable" = "0" ]; then
			ifconfig rai0 up
		fi	
	fi
		
fi
