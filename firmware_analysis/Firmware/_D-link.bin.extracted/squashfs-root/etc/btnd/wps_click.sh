echo "gpio btn wps!"

if [ -f "/var/btn_test" ];then
		touch /var/btn_wps_ok
		return
fi

iwpriv ra0 set WscConfMode=7
iwpriv ra0 set WscMode=2
iwpriv ra0 set WscGetConf=1

iwpriv rai0 set WscConfMode=7
iwpriv rai0 set WscMode=2
iwpriv rai0 set WscGetConf=1

/bin/wsc_monitor.sh 120 ra0 rai0 &





