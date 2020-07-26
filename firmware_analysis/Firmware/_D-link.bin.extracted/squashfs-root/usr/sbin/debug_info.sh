#! /bin/sh

# remove debug_info folder
rm -rf /var/log/debug_info

# mkdir debug_info folder
mkdir /var/log/debug_info

# add debug cmd
cat /proc/meminfo > /var/log/debug_info/meminfo
ps > /var/log/debug_info/runtimestat
ifconfig >> /var/log/debug_info/runtimestat
iwpriv ra0 show stainfo >> /var/log/debug_info/runtimestat
iwconfig >> /var/log/debug_info/runtimestat 2>&1
brctl show >> /var/log/debug_info/runtimestat
brctl showmacs br-lan >> /var/log/debug_info/runtimestat
cat /proc/portal_manage >> /var/log/debug_info/runtimestat 
#collect plc log
plclog -i br-lan -x > /var/log/debug_info/plclog.xlog  2>&1
plclog -i br-lan -q > /var/log/debug_info/plclog.log   2>&1
plctool -i br-lan -m > /var/log/debug_info/plctool.log 2>&1



