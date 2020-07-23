#!/bin/bash

##########################################################################################################################
#
# place in: /usr/lib/check_mk_agent/local
# and make executable
#
##########################################################################################################################

array=("gsad.service" "gvmd.service" "ospd-openvas.service" "redis-server@openvas.service")
for item in ${array[*]}
do
    if [ `systemctl is-active $item` = "active" ] ; then
      echo "0 openvas_svc_$item - $item active"
    else
      echo "2 openvas_svc_$item - $item inactive"
    fi
done

