#!/usr/bin/python
import os, sys, subprocess, shlex, re, fnmatch,signal
from subprocess import call
import smtplib
import threading
import time
import MySQLdb as mdb
import urllib, json
#POST, PUT json data
import requests
#/monitor/write_temp.py
from write_temp import *

def connect_mysql_db(host,port,user,password,db):
    return mdb.connect(host=host,port=port,user=user,passwd=password,db=db)

###############################################################################
#Use Ffprobe to check stastus profile (source) and return flag                #
#0 is down                                                                    #
#1 is up                                                                      #
#2 is video error                                                             #
#3 is audio eror                                                              #
###############################################################################

def probe_file(source):
    cmnd = ['/usr/local/bin/ffprobe', source, '-v', 'quiet' , '-show_format', '-show_streams', '-timeout', '60']
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = 30
    i = 0
    while p.poll() is None:
        time.sleep(1)
        i+=1
        if i > timeout:
            os.kill(p.pid, signal.SIGKILL)
    out, err = p.communicate()
    value=0
    audio=0
    video=0
    for line in out.split('\n'):
        line = line.strip()
        if (line.startswith('filename=')):
            value=1
        if (line.startswith('codec_type=audio')):
            audio=1
        if (line.startswith('codec_type=video')):
            video=1
    if value == 1 and audio == 1 and video == 1:
        return 1
    if value == 1 and audio == 1 and video == 0:
        return 2
    if value == 1 and audio == 0 and video == 1:
        return 3
    return 0
###############################################################################
#                                                                             #
#Get status of profile, if stastus not change then update check equal 1.      #
#                                                                             #
###############################################################################

def check_probe(profile,value,id,thread,name,type):
    check = probe_file(profile)
    print "%s : %s"%(check,value)
    if check != value:
        tmp="""{"source":"%s","status":%s,"pa_id":%s,"thread":%s,"name":"%s","type":"%s"}"""%(profile,value,id,thread,name,type)
        File().append(tmp)

###############################################################################
#                                                                             #
#                                 MAIN                                        #
#                                                                             #
###############################################################################
configfile='/monitor/config/config.py'
if os.path.exists(configfile):
    execfile(configfile)
else:
    print "can't read file config"
    exit(1)

def sql_data():
    print "sql"
    session=connect_mysql_db(hostDB,port,user,password,db);
    cur=session.cursor();
    query="select pa.id,p.ip,p.protocol,pa.status,a.thread,c.name,p.type from profile as p, agent as a, profile_agent as pa,channel as c where pa.profile_id=p.id and pa.agent_id=a.id and a.active=1 and pa.monitor=1 and p.channel_id=c.id and a.ip='" + ip +"'"
    cur.execute(query)
    rows = cur.fetchall()
    session.close()
    for row in rows:
        while threading.activeCount() > row[4]:
            time.sleep(1)
        t = threading.Thread(target=check_probe, args=(row[2]+'://'+row[1],row[3],row[0],row[4],row[5],row[6],))
        t.start()


try:
    response = urllib.urlopen(api+"profile_agent/"+ip+"/")
    if response.getcode()==200:
        print "200"
        profile_agents = json.loads(response.read())
        for profile_agent in profile_agents['agent']:
#            print str(threading.activeCount()) +":"+ str(threading.activeCount())
            while threading.activeCount() > profile_agent['thread']:
                time.sleep(2)
            t = threading.Thread(target=check_probe, args=(profile_agent['protocol']+'://'+profile_agent['ip'],profile_agent['status'],profile_agent['id'],profile_agent['thread'],profile_agent['name'],profile_agent['type'],))
            t.start()
    elif response.getcode()==404 or response.getcode()==502:
        sql_data()
except:
    try:
        sql_data()
    except Exception as e:
        print e
finally:
    #Wait for all threads finish
    time.sleep(45)


