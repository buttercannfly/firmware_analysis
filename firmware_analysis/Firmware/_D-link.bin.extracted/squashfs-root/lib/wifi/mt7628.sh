#!/bin/sh
append DRIVERS "mt7628"

. /lib/wifi/ralink_common.sh

prepare_mt7628() {
	prepare_ralink_wifi mt7628
}

scan_mt7628() {
	scan_ralink_wifi mt7628 mt7628
}


disable_mt7628() {
	disable_ralink_wifi mt7628
}

enable_mt7628() {
	enable_ralink_wifi mt7628 mt7628
}

detect_mt7628() {
#	detect_ralink_wifi mt7628 mt7628
	ssid=mt7628-`ifconfig eth0 | grep HWaddr | cut -c 51- | sed 's/://g'`
	cd /sys/module/
	[ -d $module ] || return
	[ -e /etc/config/wireless ] && return
         cat <<EOF
config wifi-device      mt7628
        option type     mt7628
        option vendor   ralink
        option band     2.4G
        option channel  0
        option autoch   3
	option wifimode 9
        option bw       0
        option ht_bsscoexist 1
        option wmm      0
        option ht_gi    1
        option txpower  100
        option country CN
        option region 1
        option ht_txstream 2
        option ht_rxstream 2
        option bandsteering 0
        option txpreamble 1
        option ht_extcha 0
        option autoch_skip '12;13'
	option e2paccmode 2

config wifi-iface
        option device   mt7628
        option ifname   ra0
        option network  lan
        option mode     ap
        option disabled   0
        option ssid     $ssid
        option hidden   0
        option encryption none
        option key      12345678
		option charcode utf-8		
        option last_maclist_mode 2
        option maclist_mode 0
        option maclist  

config wifi-iface
        option device   mt7628
        option ifname   ra1
        option network  guest
        option mode     ap
        option disabled   1
        option ssid     guest-$ssid
        option hidden   0
        option encryption none
        option key      12345678
		option charcode utf-8		
        option maclist_mode 0
        option maclist  

config wifi-iface       apcli0
        option device 	mt7628
        option ifname 	apcli0
        option network 	lan
        option mode    	sta
        option disabled     1
        option apcli_enable 0
        option apcli_ssid ''
        option rootap_bssid '00:00:00:00:00:00'
        option apcli_authmode OPEN
        option apcli_encryptype NONE
        option apcli_wpapsk ''
        option apcli_key1type 1
        option apcli_key1str ''		
EOF


}


