#!/usr/bin/python
class File:
    def __init__(self):
        self.filedir= "./config/config.py"

    def append(self, host = None, masterdb = None, masterapi = None, slaveapi = None):
        str = """SYSTEM = {\n
    "HOST":"%s",\n
    "monitor": {\n
        "SOURCE": True,\n
        "BLACK_SCREEN": False\n
    },\n
\n
    "broadcast_time": {\n
        "FROM": 6,\n
        "TO": 22\n
    },\n
\n
    "libery": {\n
        "FFPROBE": "/usr/local/bin/ffprobe",\n
        "FFMPEG": "/opt/ffmpeg/ffmpeg"\n
    },\n
    "BREAK_TIME": 20\n
}\n
\n
API = {\n
    "master": {\n
        "URL": "%s",\n
        "PORT": 8888,\n
        "USER": "monitor",\n
        "PASSWORD": "iptv13579"\n
    },\n
\n
    "slave": {\n
        "ACTIVE" : False,\n
        "URL": "%s",\n
        "PORT": 8888,\n
        "USER": "monitor",\n
        "PASSWORD": "iptv13579"\n
    }\n
}\n
\n
DATABASE = {\n
    "master": {\n
        "ACTIVE" : True,\n
        "HOST": "%s",\n
        "NAME": "monitor",\n
        "USER": "MonitorAgent",\n
        "PASSWORD": "11nit0rA93nt",\n
        "PORT": 3306\n
    },\n
\n
    "slave": {\n
        "ACTIVE" : False,\n
        "HOST": "localhost",\n
        "NAME": "monitor",\n
        "USER": "root",\n
        "PASSWORD": "root",\n
        "PORT": 3306\n
    }\n
}\n
\n
LOGGING = {\n
    "version": 1,\n
    "disable_existing_loggers": False,\n
    "formatters": {\n
        "simple": {\n
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"\n
        }\n
    },\n
\n
    "handlers": {\n
        "file_handler": {\n
            "class": "logging.FileHandler",\n
            "level": "DEBUG",\n
            "formatter": "simple",\n
            "filename": "/var/log/monior_IPTV.log",\n
            "encoding": "utf8"\n
        }\n
    },\n
\n
    "root": {\n
        "level": "DEBUG",\n
        "handlers": ["file_handler"]\n
    }\n
}\n
\n
"""%(host, masterapi, slaveapi, matserdb)
        f = open(self.filedir, 'w')
        f.write(str+"\n")
        f.close()
