#!/bin/sh
append DRIVERS "mt7612e"

. /lib/wifi/ralink_common.sh

prepare_mt7612e() {
	prepare_ralink_wifi mt7612e
}

scan_mt7612e() {
	scan_ralink_wifi mt7612e mt76x2e
}

disable_mt7612e() {
	disable_ralink_wifi mt7612e
}

enable_mt7612e() {
	enable_ralink_wifi mt7612e mt76x2e
}

detect_mt7612e() {
#	detect_ralink_wifi mt7612e mt76x2e
	ssid=mt7612e #-`ifconfig eth0 | grep HWaddr | cut -c 51- | sed 's/://g'`
	cd /sys/module/
	[ -d $module ] || return
	[ -e /etc/config/wireless ] && return
	 cat <<EOF
config wifi-device      mt7612e
        option type     mt7612e
        option vendor   ralink
        option band     5G
        option channel  0
        option autoch   1
        option wifimode 14
        option bw       2
        option wmm      0
        option vht_sgi    1
        option txpower  100
        option country CN
        option aregion 10  
	option txpreamble 1
        option ht_bsscoexist 0
	option bandsteering 0
	option autoch_skip 165
	option e2paccmode 2

config wifi-iface
        option device   mt7612e
        option ifname   rai0
        option network  lan
        option mode     ap
        option disabled  0
        option ssid     $ssid
        option hidden   0
        option encryption none
        option key      12345678
		option charcode utf-8		
        option maclist_mode 0
        option maclist  

config wifi-iface
        option device   mt7612e
        option ifname   rai1
        option network  guest
        option disabled  1
        option mode     ap
        option ssid     $ssid
        option hidden   0
        option encryption none
        option key      12345678
		option charcode utf-8		
        option maclist_mode 0
        option maclist  

config wifi-iface       apclii0
        option device 	mt7612e
        option ifname 	apclii0
        option network 	lan
        option mode    	sta
        option disabled     1
        option apcli_enable 0
        option apcli_ssid ''
        option rootap_bssid '00:00:00:00:00:00'
        option apcli_authmode ''
        option apcli_encryptype ''
        option apcli_wpapsk ''
        option apcli_key1type 1
        option apcli_key1str ''


EOF

}


