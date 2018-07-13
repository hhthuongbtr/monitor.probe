from fabric.api import local, run, env, put
import os, time

# remote ssh credentials
#test
env.hosts = ['118.69.132.98']

#HCM
#env.hosts = ['172.28.0.102', '172.28.0.106', '172.28.0.110',\
# '172.28.0.114', '172.28.0.118', '172.28.0.122',\
# '172.28.0.126', '172.28.0.202', '172.28.0.206',\
# '172.28.0.210', '172.28.0.214', '172.28.0.218',\
# '172.28.0.86', '172.28.0.90', '172.28.0.94', '172.28.0.98'\
# '172.28.0.86', '172.28.0.90', '172.28.0.94', '172.28.0.98']

#HNI
#env.hosts = ['42.112.0.234', '42.112.0.238',\
# '42.114.247.130', '42.114.247.134', '42.114.247.138',\
# '42.114.247.142', '42.114.247.150', '42.114.247.154']

#proxy pass 118.69.190.70
#env.hosts = ['172.28.0.38', '172.28.0.42',\
# '172.28.0.74', '172.28.0.78']


env.user = 'root'
env.password = 'Passonetv#@!' #ssh password for user
# or, specify path to server public key here:
# env.key_filename = ''

# specify path to deploy root dir - you need to create this
env.deploy_project_root = '/monitor/'

def create_config_folder():
        # create config folder
        print('create config folder...')
        run('mkdir %s && mkdir %s && mkdir %s && cp %s %s' \
                % (env.deploy_project_root+"monitor", env.deploy_project_root+"config", env.deploy_project_root+"releases", env.deploy_project_root+"config.py", env.deploy_project_root+"config"))
        #print('remove file')
        #run('rm -rf %s' \
        #        % (env.deploy_project_root+"*.*"))

def deploy():
        create_config_folder()
        print('deploy complete!')
