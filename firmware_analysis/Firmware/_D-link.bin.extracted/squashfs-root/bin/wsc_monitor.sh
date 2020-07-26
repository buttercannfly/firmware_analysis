#!/bin/sh
timeOut=$1
success_wps=0
STATUS_WSC_USER_IDEL=0
STATUS_WSC_USER_SUCCESS=1
STATUS_WSC_USER_TIMEOUT=2
STATUS_WSC_USER_OVERLAP=3

wlan_wps_ap_stop_mtk()
{
	iwpriv $1 set WscStop=1
	iwpriv $2 set WscStop=1
	# WscStop=1 will cause device stop bring wps information in beacon, so we set it again                    
	#iwpriv $1 set WscConfMode=7                 
	#iwpriv $2 set WscConfMode=7                 

}	

wlan_wps_ap_success_mtk()
{
	echo "WPS Success"

	echo "1" > /var/wps_status	
	
	wlan_wps_ap_stop_mtk $1 $2
    #Set WiFi LED
	gpio l 37 50 1 1 1 1 
}

wlan_wps_ap_overlap_mtk()
{
	echo "WPS Overlap"

	echo "2" > /var/wps_status

	wlan_wps_ap_stop_mtk $1 $2
    #Set WiFi LED to "Green ON" when WPS overlap
    gpio l 37 1 1 1 1 1
}

wlan_wps_ap_timeout_mtk()
{
	echo "WPS Timeout"

	echo "3" > /var/wps_status

	wlan_wps_ap_stop_mtk $1 $2
    #Set WiFi LED to "Green ON" when WPS timeout
    gpio l 37 1 1 1 1 1
}


if [ "$1" == "" ]; then
#default time is 120 sec.
timeOut=120
fi
while [ "$timeOut" -ne "0" ]
do

if [ "$timeOut" -eq "120" ]; then
gpio l 37 2 1 4000 1 4000
fi

statusWsc=`cat /proc/wsc/wsc_status`
statusWsc5g=`cat /proc/wsc5g/wsc_status5g`
echo "WSC status is $statusWsc"
echo "WSC status5g is $statusWsc5g"
if [ "$statusWsc" == "$STATUS_WSC_USER_SUCCESS" ]; then
wlan_wps_ap_success_mtk $2 $3
echo 0 > /proc/wsc/wsc_status
success_wps=1
break
fi
if [ "$statusWsc5g" == "$STATUS_WSC_USER_SUCCESS" ]; then
wlan_wps_ap_success_mtk $2 $3
echo 0 > /proc/wsc5g/wsc_status5g
success_wps=1
break
fi

if [ "$statusWsc" == "$STATUS_WSC_USER_TIMEOUT" ]; then
wlan_wps_ap_timeout_mtk $2 $3
echo 0 > /proc/wsc/wsc_status
break
fi
if [ "$statusWsc5g" == "$STATUS_WSC_USER_TIMEOUT" ]; then
wlan_wps_ap_timeout_mtk $2 $3
echo 0 > /proc/wsc5g/wsc_status5g
break
fi

if [ "$statusWsc" == "$STATUS_WSC_USER_OVERLAP" ]; then
wlan_wps_ap_overlap_mtk $2 $3
echo 0 > /proc/wsc/wsc_status
break
fi
if [ "$statusWsc5g" == "$STATUS_WSC_USER_OVERLAP" ]; then
wlan_wps_ap_overlap_mtk $2 $3
echo 0 > /proc/wsc5g/wsc_status5g
break
fi

timeOut=`expr $timeOut - 1`
sleep 1
done
if [ "$timeOut" -eq "0" ]; then
wlan_wps_ap_timeout_mtk $2 $3
echo 0 > /proc/wsc/wsc_status
echo 0 > /proc/wsc5g/wsc_status5g
fi

#init status
echo 0 > /proc/wsc/wsc_status
echo 0 > /proc/wsc5g/wsc_status5g

# success continue 120 sec
if [ "$success_wps" -eq "1" ];then
timeOut=120
fi

while [ "$timeOut" -ne "0" ];
do
timeOut=`expr $timeOut - 1`
sleep 1
done

#gpio l 3 0 4000 0 1 4000
network_status=`cat /var/wan_abnormal_reason | grep 0 | wc -l`

if [ "$success_wps" -eq "0" ];then
#gpio l 3 4 0 1 0 4000
fi

if [ "$success_wps" -eq "1" ];then
#gpio l 3 4000 0 1 0 4000
fi



