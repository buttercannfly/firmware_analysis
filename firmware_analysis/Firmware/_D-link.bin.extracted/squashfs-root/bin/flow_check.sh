#! /bin/sh

rm -f /var/flow.txt

echo -n "flow check start time: " >/var/flow.txt
date +'%Y-%m-%d %T' >>/var/flow.txt

network_mode=`uci get network.globals.network_mode`

record_flow()
{
	if [ "$network_mode" != "repeater" ]
	then
		ifconfig $wan_ifname |grep "RX bytes:" >>/var/flow.txt
	else
		Rx=`iwpriv $wan_ifname stationcountinfo|grep $wan_ifname|awk '{print $6}'`
		Tx=`iwpriv $wan_ifname stationcountinfo|grep $wan_ifname|awk '{print $5}'`
		if [ Rx = "" -o Tx = "" ]
		then 
			echo "          RX bytes:0  TX bytes:0" >>/var/flow.txt
		fi 
		
		TotalRx=0
		TotalTx=0

		for rx in $Rx
		do
			TotalRx=`expr $TotalRx + $rx`

		done
		
		for tx in $Tx
		do
			TotalTx=`expr $TotalTx + $tx`

		done
		echo "          RX bytes:$TotalRx  TX bytes:$TotalTx" >>/var/flow.txt
	fi 
}

if [ "$network_mode" != "repeater" ]
then
	wan_ifname=`uci get global_readonly.globals.wan_ifname`
else
	repeater_use_24g=`uci get wireless.apcli0.apcli_enable`
	if [ "$repeater_use_24g" = "" ]
	then
		exit
	fi 
		
	if [ "$repeater_use_24g" = "1" ]
	then
		wan_ifname=`uci get global_readonly.globals.repeater_24g_ifname`
	else
		wan_ifname=`uci get global_readonly.globals.repeater_5g_ifname`
	fi
fi

if [ "$wan_ifname" = "" ]
then
	exit
fi

for index in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
	record_flow
	sleep 60
done

record_flow
