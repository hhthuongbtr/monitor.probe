from fabric.api import local, run, env, put
import os, time
from create_config import *

# remote ssh credentials
#test
#env.hosts = ['172.28.0.214', '172.28.0.218']

#HCM
#env.hosts = ['172.28.0.102', '172.28.0.106', '172.28.0.110',\
# '172.28.0.114', '172.28.0.118', '172.28.0.122',\
# '172.28.0.126', '172.28.0.202', '172.28.0.206',\
# '172.28.0.210', '172.28.0.214', '172.28.0.218']
# '172.28.0.86', '172.28.0.90', '172.28.0.94', '172.28.0.98']

#DB HNI
#env.hosts = ['42.114.247.150']
#env.hosts = ['42.112.0.234', '42.112.0.238',\
# '42.114.247.130', '42.114.247.134',\
# '42.114.247.138', '42.114.247.150']

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
env.archive_name = 'temp_config'

# specify path to deploy root dir - you need to create this
env.deploy_project_root = '/monitor/config/'

#fluentd host
env.hostDB = '118.69.166.134'

#api host
env.api = 'http://42.117.9.99:8888/'

def create_config_file():
        print('Create config file...')
        File().append(env.host, env.hostDB, env.api)

def update_local_copy():
        # get latest / desired tag from your version control system
        print('updating local copy...')

def upload_archive():
        # create archive from env.archive_source
        print('creating archive...')
        local('cd %s && zip -qr %s.zip config.py' \
                % (env.archive_source, env.archive_name))

        print('remove old config.py file')
        run('rm -rf %s' \
                % (env.deploy_project_root+"config.py"))

        # create time named dir in deploy dir
        print('uploading archive...')
        run('cd %s' % (env.deploy_project_root))

        # extract code into dir
        print('extracting code...')
        put(env.archive_name+'.zip', env.deploy_project_root)
        run('cd %s && unzip -q %s.zip -d . && rm %s.zip' \
                % (env.deploy_project_root, env.archive_name, env.archive_name))

def cleanup():
        # remove any artifacts of the deploy process
        print('cleanup...')
        local('rm -rf %s.zip' % env.archive_name)

def deploy():
        create_config_file()
        update_local_copy()
        upload_archive()
        cleanup()
        print('deploy complete!')
