#!/bin/sh
#
#wifi_down.sh
#
#useing:crond for wifi down
#

ntp_flag=`cat /var/ntpd_sync`
network_mode=`uci get network.globals.network_mode`

if [ "$ntp_flag" = "1" ]; then
	if [ ${network_mode} = "repeater" ]; then
		ifconfig ra0 down
		ifconfig rai0 down
	else
		wifi down
	fi
	
fi

