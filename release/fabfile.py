from fabric.api import local, run, env, put
import os, time

# remote ssh credentials
#test
env.hosts = ['10.0.200.30']

#HCM
#env.hosts = ['172.28.0.102', '172.28.0.106', '172.28.0.110',\
# '172.28.0.114', '172.28.0.118', '172.28.0.122',\
# '172.28.0.126', '172.28.0.202', '172.28.0.206',\
# '172.28.0.210', '172.28.0.214', '172.28.0.218',\
# '172.28.0.86', '172.28.0.90', '172.28.0.94', '172.28.0.98']

#DB HNI

#env.hosts = ['42.112.0.234', '42.112.0.238',\
# '42.114.247.130', '42.114.247.134',\
# '42.114.247.138', '42.114.247.150',\
# '172.29.71.27', '172.29.71.19']

#HNCORE
#env.hosts = ['42.114.247.21', '42.114.247.22']

#proxy pass 118.69.190.70
#env.hosts = ['172.28.0.38', '172.28.0.42',\
# '172.28.0.74', '172.28.0.78']

env.user = 'root'
env.password = 'Passonetv#@!' #ssh password for user
# or, specify path to server public key here:
# env.key_filename = ''

# specify path to files being deployed
env.archive_source = '.'

# archive name, arbitrary, and only for transport
env.archive_name = 'temp_monitor'

# specify path to deploy root dir - you need to create this
env.deploy_project_root = '/monitor/'

# specify name of dir that will hold all deployed code
env.deploy_release_dir = '/usr/share/monitor/'

# symlink name. Full path to deployed code is env.deploy_project_root + this
env.deploy_current_dir = 'monitor'

env.SYSTEM = {
    "HOST":"0.0.0.0",
    "monitor": {
        "SOURCE": True,
        "BLACK_SCREEN": False
    },

    "broadcast_time": {
        "FROM": 6,
        "TO": 22
    },

    "libery": {
        "FFPROBE": "/usr/local/bin/ffprobe",
        "FFMPEG": "/opt/ffmpeg/ffmpeg"
    },
    "BREAK_TIME": 20
}

env.API = {
    "master": {
        "URL": "10.0.200.99",
        "PORT": 8888,
        "USER": "monitor",
        "PASSWORD": "iptv13579"
    },

    "slave": {
        "ACTIVE" : False,
        "URL": "42.117.9.100",
        "PORT": 8888,
        "USER": "monitor",
        "PASSWORD": "iptv13579"
    }
}

env.DATABASE = {
    "master": {
        "ACTIVE" : True,
        "HOST": "10.0.200.32",
        "NAME": "monitor",
        "USER": "MonitorAgent",
        "PASSWORD": "11nit0rA93nt",
        "PORT": 3306
    },

    "slave": {
        "ACTIVE" : False,
        "HOST": "localhost",
        "NAME": "monitor",
        "USER": "root",
        "PASSWORD": "root",
        "PORT": 3306
    }
}

env.LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "/var/log/monior_IPTV.log",
            "encoding": "utf8"
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["file_handler"]
    }
}


def create_config_file():
        print('Create config file...')
        env.SYSTEM["HOST"] = env.host
        text = "SYSTEM = " + str(env.SYSTEM)
        text = text + "\n" + "API = " + str(env.API)
        text = text + "\n" + "DATABASE = " + str(env.DATABASE)
        text = text + "\n" + "LOGGING = " + str(env.LOGGING)
        f = open("./config/config.py", 'w')
        f.write(text)
        f.close()

def update_local_copy():
        # get latest / desired tag from your version control system
        print('updating local copy...')

def upload_archive():
        # create archive from env.archive_source
        print('creating archive...')
        local('cd %s && zip -qr %s.zip -x=fabfile.py -x=fabfile.pyc -x=create_config.py -x=create_config.pyc *' \
                % (env.archive_source, env.archive_name))

        # Create monitor
        print('Create /usr/share/monitor folder...')
        run('mkdir -p %s' % (env.deploy_release_dir))

        # create time named dir in deploy dir
        print('uploading archive...')
        deploy_timestring = time.strftime("%Y%m%d%H%M%S")
        run('cd %s && mkdir %s' % (env.deploy_release_dir, deploy_timestring))

        # extract code into dir
        print('extracting code...')
        env.deploy_full_path = env.deploy_release_dir + deploy_timestring
        put(env.archive_name+'.zip', env.deploy_full_path)
        run('cd %s && unzip -q %s.zip -d . && rm %s.zip' \
                % (env.deploy_full_path, env.archive_name, env.archive_name))

def before_symlink():
        # code is uploaded, but not live. Perform final pre-deploy tasks here
        print('before symlink tasks...')

def make_symlink():
        # delete existing symlink & replace with symlink to deploy_timestring dir
        print('creating symlink to uploaded code...')
        run('rm -rf %s' % env.deploy_project_root)
        run('mkdir -p %s' % (env.deploy_project_root))
        run('ln -s %s/* %s' % (env.deploy_full_path, env.deploy_project_root))

def after_symlink():
        # code is live, perform any post-deploy tasks here
        print('after symlink tasks...')

def cleanup():
        # remove any artifacts of the deploy process
        print('cleanup...')
        local('rm -rf %s.zip' % env.archive_name)

def deploy():
        create_config_file()
        update_local_copy()
        upload_archive()
        before_symlink()
        make_symlink()
        after_symlink()
        cleanup()
        print('deploy complete!')
