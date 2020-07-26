#linsd add for wifi button
echo "gpio btn wifi!"

if [ -f "/var/btn_test" ];then
		touch /var/btn_wifi_ok
		return
fi

local wlan0_dis=$(uci get wireless.@wifi-iface[0].disabled)
local wlan1_dis=$(uci get wireless.@wifi-iface[3].disabled)
	
if [ "$wlan0_dis" = "0" -o "$wlan1_dis" = "0" ]; then
		uci set wireless.@wifi-iface[0].disabled=1
		uci set wireless.@wifi-iface[3].disabled=1
		uci commit
		wifi down 
		sleep 1
		wifi up
elif [ "$wlan0_dis" = "1" -a "$wlan1_dis" = "1" ]; then
		uci set wireless.@wifi-iface[0].disabled=0
		uci set wireless.@wifi-iface[3].disabled=0
		uci commit
		wifi down 
		sleep 1
		wifi up
fi
