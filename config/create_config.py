#!/usr/bin/python
class File:
    def __init__(self):
        self.filedir= "./config.py"

    def append(self, host, hostDB, api):
        str = "#!/usr/bin/python\n\
api='%s'\n\
hostDB='%s'\n\
host=hostDB\n\
port=3306\n\
user='MonitorAgent'\n\
password='11nit0rA93nt'\n\
db='monitor'\n\
ip='%s'\n\
snmp_host='localhost'\n\
snmp_port=161\n\
snmp_community='public'\n\
timewait=5\n\
"%(api, hostDB, host)
        f = open(self.filedir, 'w')
        f.write(str+"\n")
        f.close()
