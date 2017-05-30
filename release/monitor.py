#!/usr/bin/python
import os, sys, subprocess, shlex, re, fnmatch,signal
import psutil
import urllib, json
#POST, PUT json data
import requests

configfile='/monitor/config/config.py'
if os.path.exists(configfile):
    execfile(configfile)
else:
    print "can't read file config"
    exit(1)

def get_mem_percent():
    info=str(psutil.virtual_memory())
    percent = info[info.find("percent=")+8 : len(info)]
    mem = percent[0 : percent.find(",")]
    mem = mem if len(mem) <=5 else percent[0 : 5]
    try:
        mem = int(round(float(mem),0))
        return mem
    except Exception:
        return -1

def get_disk_percent():
    info=str(psutil.disk_usage('/'))
    percent = info[info.find("percent=")+8 : len(info)]
    disk = percent[0 : percent.find(",")]
    disk = disk if len(disk) <=5 else percent[0 : 5]
    try:
        disk=int(round(float(disk),0))
        return disk
    except Exception:
        return -1

def get_cpu_percent():
    try:
        cpu=int(round( psutil.cpu_percent(interval=1), 0))
        return cpu
    except Exception:
        return -1
requests.put(api+"agent/"+ip+"/", json={"cpu": get_cpu_percent(),"mem":get_mem_percent(),"disk":get_disk_percent()})
