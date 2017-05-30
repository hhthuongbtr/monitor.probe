#!/bin/bash
/usr/bin/python /monitor/monitor/snmp_agent.py > /dev/null
sleep 10
/usr/bin/python /monitor/monitor/monitor.py > /dev/null

