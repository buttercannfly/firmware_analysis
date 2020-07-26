echo "gpio btn reset!"

        if [ -f "/var/btn_test" ];then
                touch /var/btn_test_ok
                return
        fi
jffs2reset -y
reboot


