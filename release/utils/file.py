import os

class File:
    def __init__(self):
        self.filedir= "/tmp/checkdata.tmp"
        self.inprocess="/tmp/inprocess.tmp"
        if not os.path.exists(self.filedir):
            command="echo '\n' >"+self.filedir
            os.system(command)
        if not os.path.exists(self.inprocess):
            command="echo '\n' >"+self.inprocess
            os.system(command)

    def read(self):
        #Read file checkdata.tmp
        f = open(self.filedir, 'r')
        lines=f.read()
        f.close()
        #Clear checkdata.tmp after read
        command="cat /dev/null > "+self.filedir
        os.system(command)
        #clear all and write data to inprocess file
        command="cat /dev/null > "+self.inprocess
        os.system(command)
        f = open(self.inprocess, 'a')
        f.write(lines)
        f.close()
        #return data
        return lines

    def append(self, text):
        f = open(self.filedir, 'r')
        data_rows = f.read()
        f.close()
        fips = open(self.inprocess, 'r')
        data_ips = fips.read()
        fips.close()
        if (text not in data_rows)and (text not in data_ips):
            f = open(self.filedir, 'a')
            f.write(text+"\n")
            f.close()
            return 0
        else:
            print "replicate"
            return 1

class Snmp:
    def __init__(self):
        self.agent_channel_status = "/monitor/snmp/agent/channel_status"
        self.agent_channel_name = "/monitor/snmp/agent/channel_name"
        self.agent_channel_profile = "/monitor/snmp/agent/channel_profile"
        self.analyzer_channel_status = "/monitor/snmp/analyzer/channel_status"
        self.analyzer_channel_name = "/monitor/snmp/analyzer/channel_name"
        self.analyzer_channel_profile = "/monitor/snmp/analyzer/channel_profile"

    def read_profile(self, file_path = None):
        file_path = self.channel_profile
        with open(file_path, "r") as text_file:
            return text_file.read()

    def read_status(self, file_path = None):
        file_path = self.channel_status
        with open(file_path, "r") as text_file:
            return text_file.read()

    def read_name(self, file_path = None):
        file_path = self.channel_name
        with open(file_path, "r") as text_file:
            return text_file.read()

    def update_agent_profile(self, text = None):
        f = open(self.agent_channel_profile, 'w')
        f.write(text)
        f.close()
        return 0

    def update_agent_status(self, text = None):
        f = open(self.agent_channel_status, 'w')
        f.write(text)
        f.close()
        return 0

    def update_agent_name(self, text = None):
        f = open(self.agent_channel_name, 'w')
        f.write(text)
        f.close()
        return 0

    def update_analyzer_profile(self, text = None):
        f = open(self.analyzer_channel_profile, 'w')
        f.write(text)
        f.close()
        return 0

    def update_analyzer_status(self, text = None):
        f = open(self.analyzer_channel_status, 'w')
        f.write(text)
        f.close()
        return 0

    def update_analyzer_name(self, text = None):
        f = open(self.analyzer_channel_name, 'w')
        f.write(text)
        f.close()
        return 0
