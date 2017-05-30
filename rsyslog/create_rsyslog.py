#!/usr/bin/python
class File:
    def __init__(self):
        self.filedir= "./rsyslog.conf"

    def append(self, host, fluentd):
    	str = "# rsyslog v5 configuration file\n\
\n\
# For more information see /usr/share/doc/rsyslog-*/rsyslog_conf.html\n\
# If you experience problems, see http://www.rsyslog.com/doc/troubleshoot.html\n\
\n\
#### MODULES ####\n\
$LocalHostName %s\n\
$ModLoad imuxsock # provides support for local system logging (e.g. via logger command)\n\
$ModLoad imklog   # provides kernel logging support (previously done by rklogd)\n\
#$ModLoad immark  # provides --MARK-- message capability\n\
\n\
# Provides UDP syslog reception\n\
#$ModLoad imudp\n\
#$UDPServerRun 514\n\
\n\
# Provides TCP syslog reception\n\
#$ModLoad imtcp\n\
#$InputTCPServerRun 514\n\
\n\
\n\
#### GLOBAL DIRECTIVES ####\n\
\n\
# Use default timestamp format\n\
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat\n\
\n\
# File syncing capability is disabled by default. This feature is usually not required,\n\
# not useful and an extreme performance hit\n\
#$ActionFileEnableSync on\n\
\n\
# Include all config files in /etc/rsyslog.d/\n\
$IncludeConfig /etc/rsyslog.d/*.conf\n\
\n\
\n\
#### RULES ####\n\
\n\
# Log all kernel messages to the console.\n\
# Logging much else clutters up the screen.\n\
#kern.*                                                 /dev/console\n\
\n\
# Log anything (except mail) of level info or higher.\n\
# Don't log private authentication messages!\n\
*.info;mail.none;authpriv.none;cron.none                /var/log/messages\n\
\n\
# The authpriv file has restricted access.\n\
authpriv.*                                              /var/log/secure\n\
\n\
# Log all the mail messages in one place.\n\
mail.*                                                  -/var/log/maillog\n\
\n\
\n\
# Log cron stuff\n\
cron.*                                                  /var/log/cron\n\
\n\
# Everybody gets emergency messages\n\
*.emerg                                                 *\n\
\n\
# Save news errors of level crit and higher in a special file.\n\
uucp,news.crit                                          /var/log/spooler\n\
\n\
# Save boot messages also to boot.log\n\
local7.*                                                /var/log/boot.log\n\
*.*                                                     @@%s\n\
\n\
# ### begin forwarding rule ###\n\
# The statement between the begin ... end define a SINGLE forwarding\n\
# rule. They belong together, do NOT split them. If you create multiple\n\
# forwarding rules, duplicate the whole block!\n\
# Remote Logging (we use TCP for reliable delivery)\n\
#\n\
# An on-disk queue is created for this action. If the remote host is\n\
# down, messages are spooled to disk and sent when it is up again.\n\
#$WorkDirectory /var/lib/rsyslog # where to place spool files\n\
#$ActionQueueFileName fwdRule1 # unique name prefix for spool files\n\
#$ActionQueueMaxDiskSpace 1g   # 1gb space limit (use as much as possible)\n\
#$ActionQueueSaveOnShutdown on # save messages to disk on shutdown\n\
#$ActionQueueType LinkedList   # run asynchronously\n\
#$ActionResumeRetryCount -1    # infinite retries if host is down\n\
# remote host is: name/ip:port, e.g. 192.168.0.1:514, port optional\n\
#*.* @@remote-host:514\n\
# ### end of the forwarding rule ###\n\
"%(host, fluentd)
        f = open(self.filedir, 'w')
        f.write(str+"\n")
        f.close()

