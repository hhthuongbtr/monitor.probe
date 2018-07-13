from fabric.api import local, run, env, put
import os, time

# remote ssh credentials
env.hosts = ['172.28.0.102', '172.28.0.106', '172.28.0.110',\
 '172.28.0.114', '172.28.0.118', '172.28.0.122',\
 '172.28.0.126', '172.28.0.202', '172.28.0.206',\
 '172.28.0.210', '172.28.0.214', '172.28.0.218',\
 '172.28.0.86', '172.28.0.90', '172.28.0.94', '172.28.0.98']

env.user = 'root'
env.password = 'Passonetv#@!' #ssh password for user
# or, specify path to server public key here:
# env.key_filename = ''

# specify path to deploy root dir - you need to create this
env.deploy_project_root = '/monitor/'

def reboot_probe():
        # create config folder
        print('probe will be reboot...')
        run('init 6')

def deploy():
        reboot_probe()
        print('deploy complete!')
