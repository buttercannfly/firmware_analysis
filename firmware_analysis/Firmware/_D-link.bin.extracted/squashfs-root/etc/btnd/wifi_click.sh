#linsd add for wifi button
echo "gpio btn wifi!"

if [ -f "/var/btn_test" ];then
		touch /var/btn_wifi_ok
		return
fi