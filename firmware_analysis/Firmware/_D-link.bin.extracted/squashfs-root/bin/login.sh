#!/bin/sh
# Copyright (C) 2006-2011 OpenWrt.org

if grep -qs '^root:[^!]' /etc/passwd /etc/shadow && [ -z "$FAILSAFE" ]; then
	echo "WARNING: telnet is a security risk"
	busybox login
else
cat << EOF
 === IMPORTANT ============================
  Use 'passwd' to set your login password
  this will enable telnet login with password
 ------------------------------------------
EOF
exec /bin/ash --login
fi
