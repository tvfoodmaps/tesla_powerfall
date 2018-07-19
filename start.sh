#!/bin/sh
# this script is started via /etc/rc.local
cd /home/pi/tesla_powerwall
python3 tesla.py > out.log 2> out.err 

