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
from write_temp import *

def connect_mysql_db(host,port,user,password,db):
    return mdb.connect(host=host,port=port,user=user,passwd=password,db=db)

def update_data(id,check,status,name,type,source):
    mgs = """%s %s (ip:%s) status %s in host: %s""" % (name, type, source, status,ip)
    try:
        aa=requests.put(api+"profile_agent/"+str(id)+"/", json={"status": check})
        print aa.status_code
        bb=requests.post(api+"log/", json={"host": source, "tag": 'status', "msg": mgs})
        #if server eror, using sql update data.
        if aa.status_code==502:
            query1="""update profile_agent set status = %s, last_update=unix_timestamp() where id=%s"""%(check,id)
            query2="""insert into logs(host,tag,datetime,msg) values ('%s','status',NOW(),'%s')"""%(source,mgs)
            print query1
            print query2
            session=connect_mysql_db(hostDB,port,user,password,db)
            cur=session.cursor()
            cur.execute(query1)
            cur.execute(query2)
            session.commit()
            session.close()
    except requests.exceptions.RequestException:
        query1="""update profile_agent set status = %s, last_update=unix_timestamp() where id=%s"""%(check,id)
        query2="""insert into logs(host,tag,datetime,msg) values ('%s','status',NOW(),'%s')"""%(source,mgs)
        print query1
        print query2
        session=connect_mysql_db(hostDB,port,user,password,db)
        cur=session.cursor()
        cur.execute(query1)
        cur.execute(query2)
        session.commit()
        session.close()

##############################################################################
#Use Ffprobe to check stastus profile (source) and return flag               #
#0 is down                                                                   #
#1 is up                                                                     #
#2 is video error                                                            #
#3 is audio eror                                                             #
##############################################################################
def probe_file(source):
    cmnd = ['/usr/local/bin/ffprobe', source, '-v', 'quiet' , '-show_format', '-show_streams']
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = 15
    i = 0
    while p.poll() is None:
        time.sleep(1)
        i+=1
        if i > timeout:
            os.kill(p.pid, signal.SIGKILL)
    out, err = p.communicate()
#    out, err =  p.communicate()
    value=0
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

##############################################################################
#Get status of profile, if stastus not change then update check equal 0 else
#recheck status if check equal recheck then update status and write log system.
##############################################################################
def check_probe(source,value,id,name,type):
    check = probe_file(source)
    print "%s : %s"%(check,value)
    if check != value:
#        time.sleep(60)
        recheck = probe_file(source)
        if recheck == check:
            if check == 1:
                status = 'up'
            elif check == 2:
                status = 'video error'
            elif check == 3:
                status = 'audio error'
            elif check == 0:
                status = 'down'
            else:
                status = "unknown" + str(check) + ":"
            update_data(id,check,status,name,type,source)

###############################################################################
#                                                                             #
#                                  MAIN                                       #
#                                                                             #
###############################################################################
configfile='/monitor/config/config.py'
if os.path.exists(configfile):
    execfile(configfile)
else:
    print "can't read file config";
    exit(1)
threads = []
data_rows=File().read()
data_rows=data_rows[0:len(data_rows)-1]
if(data_rows):
    for line in data_rows.split('\n'):
        data = json.loads(line)
        while threading.activeCount() > data['thread']:
            time.sleep(1)
        t = threading.Thread(target=check_probe, args=(data['source'],data['status'],data['pa_id'],data['name'],data['type'],))
        t.start()
        threads.append(t)
for x in threads:
        x.join()
time.sleep(5)
