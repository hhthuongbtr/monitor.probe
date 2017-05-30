from fabric.api import local, run, env, put
import os, time

# remote ssh credentials
#test
#env.hosts = ['172.28.0.214']

#HCM
#env.hosts = ['172.28.0.102', '172.28.0.106', '172.28.0.110',\
# '172.28.0.114', '172.28.0.118', '172.28.0.122',\
# '172.28.0.126', '172.28.0.202', '172.28.0.206',\
# '172.28.0.210', '172.28.0.214', '172.28.0.218',\
# '172.28.0.86', '172.28.0.90', '172.28.0.94', '172.28.0.98']

#DB HNI
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
env.archive_name = 'temp_monitor'

# specify path to deploy root dir - you need to create this
env.deploy_project_root = '/monitor/'

# specify name of dir that will hold all deployed code
env.deploy_release_dir = 'releases'

# symlink name. Full path to deployed code is env.deploy_project_root + this
env.deploy_current_dir = 'monitor'

def update_local_copy():
        # get latest / desired tag from your version control system
        print('updating local copy...')

def upload_archive():
        # create archive from env.archive_source
        print('creating archive...')
        local('cd %s && zip -qr %s.zip -x=fabfile.py -x=fabfile.pyc *' \
                % (env.archive_source, env.archive_name))

        # create time named dir in deploy dir
        print('uploading archive...')
        deploy_timestring = time.strftime("%Y%m%d%H%M%S")
        run('cd %s && mkdir %s' % (env.deploy_project_root + \
                env.deploy_release_dir, deploy_timestring))

        # extract code into dir
        print('extracting code...')
        env.deploy_full_path = env.deploy_project_root + \
                env.deploy_release_dir + '/' + deploy_timestring
        put(env.archive_name+'.zip', env.deploy_full_path)
        run('cd %s && unzip -q %s.zip -d . && rm %s.zip' \
                % (env.deploy_full_path, env.archive_name, env.archive_name))

def before_symlink():
        # code is uploaded, but not live. Perform final pre-deploy tasks here
        print('before symlink tasks...')

def make_symlink():
        # delete existing symlink & replace with symlink to deploy_timestring dir
        print('creating symlink to uploaded code...')
        run('rm -rf %s' % env.deploy_project_root + env.deploy_current_dir)
        run('ln -s %s %s' % (env.deploy_full_path, env.deploy_project_root + \
                env.deploy_current_dir))

def after_symlink():
        # code is live, perform any post-deploy tasks here
        print('after symlink tasks...')

def cleanup():
        # remove any artifacts of the deploy process
        print('cleanup...')
        local('rm -rf %s.zip' % env.archive_name)

def deploy():
        update_local_copy()
        upload_archive()
        before_symlink()
        make_symlink()
        after_symlink()
        cleanup()
        print('deploy complete!')
