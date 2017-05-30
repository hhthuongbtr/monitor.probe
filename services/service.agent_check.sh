#!/bin/sh
while [ 1 ]
do
    /usr/bin/python /monitor/monitor/agent_check.py > /dev/null
done
