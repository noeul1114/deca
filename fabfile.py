from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, local, run, sudo, require
import random
import os
import json

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Deploy = True

if Deploy:
    with open(os.path.join(PROJECT_DIR, "deploy.json")) as f:
        envs = json.loads(f.read())
else:
    with open(os.path.join(PROJECT_DIR, "deploy_2.json")) as f:
        envs = json.loads(f.read())


REPO_URL = envs['REPO_URL']
PROJECT_NAME = envs['PROJECT_NAME']
REMOTE_HOST_SSH = envs['REMOTE_HOST_SSH']
REMOTE_HOST = envs['REMOTE_HOST']
REMOTE_USER = envs['REMOTE_USER']
REMOTE_PASSWORD = envs['REMOTE_PASSWORD']
PASSWORD = envs['DB_ROOT_']

STATIC_ROOT_NAME = 'static_deploy'
STATIC_URL_NAME = 'static'
MEDIA_ROOT = 'uploads'

env.user = REMOTE_USER
username = env.user
# Option: env.password
env.hosts = [
    REMOTE_HOST_SSH,
    ]
env.password = REMOTE_PASSWORD
project_folder = '/home/{}/{}'.format(env.user, PROJECT_NAME)


apt_requirements = [
    'ufw',
    'curl',
    'git',
    'python3-dev',
    'python3-pip',
    'build-essential',
    'python3-setuptools',
    'apache2',
    'libapache2-mod-wsgi-py3',
    'libmysqlclient-dev',
    'libssl-dev',
    'libxml2-dev',
    'libjpeg8-dev',
    'zlib1g-dev',
    'postgresql',
    'goaccess',
]


def localhost():
    "Use the local virtual server"
    env.hosts = ['localhost']
    env.user = 'username'
    env.path = '/home/%(user)s/workspace/%(project_name)s' % env
    env.virtualhost_path = env.path


def test():
    sudo('mkdir testing')


def _run_as_pg(command):
    return sudo('sudo -u postgres %s' % command)


def pg_create_user(username, password):
    _run_as_pg('''psql -t -A -c "CREATE USER %(username)s WITH PASSWORD '%(password)s';"''' % locals())


def pg_create_database(database, owner):
    _run_as_pg('createdb %(database)s -O %(owner)s' % locals())


def new_server():
    setup()
    deploy()


def setup():
    _get_latest_apt()
    _install_apt_requirements(apt_requirements)
    _make_virtualenv()
    _postgres_update()
    #_ufw_allow()


def ssl_certificate():
    pass


def deploy():
    _get_latest_source()
    _put_envs()
    _update_settings()
    _update_virtualenv()
    _update_static_files()
    _update_database()
    _ufw_allow()
    # _setup_for_ssl
    # _grant_ssl_live

    # _make_virtualhost() # 처음 Virtual Host 만들때 제외하고는 실행하지 말것. Access log 초기화
    # _make_virtualhost_https()

    _grant_apache2()
    # _grant_sqlite3()
    _restart_apache2()


def _postgres_update():
    _run_as_pg('''psql -t -A -c "ALTER USER postgres with encrypted password \'{}\';"'''.format(PASSWORD))
    _run_as_pg('''psql -t -A -c "CREATE USER django PASSWORD \'{}\';"'''.format(REMOTE_PASSWORD))
    _run_as_pg('''psql -t -A -c "CREATE DATABASE sayproject;"''')
    _run_as_pg('''psql -t -A -c "GRANT ALL PRIVILEGES ON DATABASE sayproject TO django;"''')
    sudo('sudo /etc/init.d/postgresql restart')

    # sudo('sudo -u postgres psql')
    # run('ALTER USER postgres with encrypted password \'{}\';'.format(PASSWORD))
    # run('CREATE USER django PASSWORD \'{}\''.format(REMOTE_PASSWORD))
    # run('\q')
    # sudo('sudo /etc/init.d/postgresql restart')
    # sudo('sudo -u postgres createdb sayproject')

def _put_envs():
    put(os.path.join(PROJECT_DIR, 'envs.json'), '~/{}/envs.json'.format(PROJECT_NAME))


def _get_latest_apt():
    update_or_not = input('would you update?: [y/n]')
    if update_or_not=='y':
        sudo('sudo apt-get update && sudo apt-get -y upgrade')


def _install_apt_requirements(apt_requirements):
    reqs = ''
    for req in apt_requirements:
        reqs += (' ' + req)
    sudo('sudo apt-get -y install {}'.format(reqs))


def _make_virtualenv():
    if not exists('~/.virtualenvs'):
        script = '''"# python virtualenv settings
                    export WORKON_HOME=~/.virtualenvs
                    export VIRTUALENVWRAPPER_PYTHON="$(command \which python3)"  # location of python3
                    source /usr/local/bin/virtualenvwrapper.sh"'''
        run('mkdir ~/.virtualenvs')
        sudo('sudo pip3 install virtualenv virtualenvwrapper')
        run('echo {} >> ~/.bashrc'.format(script))


def _get_latest_source():
    current_commit = local('git log -n 1 --format=%H')
    if exists(project_folder + '/.git'):
        run('cd %s && git reset --hard %s' % (project_folder, current_commit))
        run('cd %s && git pull' % (project_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, project_folder))


def _update_settings():
    settings_path = project_folder + '/{}/settings.py'.format(PROJECT_NAME)
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (REMOTE_HOST,)
    )
    secret_key_file = project_folder + '/{}/secret_key.py'.format(PROJECT_NAME)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    if not exists(virtualenv_folder + '/bin/pip'):
        run('cd /home/%s/.virtualenvs && virtualenv %s' % (env.user, PROJECT_NAME))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, project_folder
    ))


def _update_static_files():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py collectstatic --noinput' % (
        project_folder, virtualenv_folder
    ))


def _update_database():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py migrate --noinput' % (
        project_folder, virtualenv_folder
    ))


def _ufw_allow():
    sudo("ufw allow 'Apache Full'")
    sudo("ufw reload")


def _make_virtualhost():
    script = """'<VirtualHost *:80>
    ServerName {servername}
    Alias /{static_url} /home/{username}/{project_name}/{static_root}
    Alias /{media_url} /home/{username}/{project_name}/{media_url}
    <Directory /home/{username}/{project_name}/{media_url}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{static_root}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{project_name}>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    WSGIDaemonProcess {project_name} python-home=/home/{username}/.virtualenvs/{project_name}/bin/ python-path=/home/{username}/{project_name}
    WSGIProcessGroup {project_name}
    WSGIScriptAlias / /home/{username}/{project_name}/{project_name}/wsgi.py
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    </VirtualHost>'""".format(
        static_root=STATIC_ROOT_NAME,
        username=env.user,
        project_name=PROJECT_NAME,
        static_url=STATIC_URL_NAME,
        servername=REMOTE_HOST,
        media_url=MEDIA_ROOT
    )
    sudo('echo {} > /etc/apache2/sites-available/{}.conf'.format(script, PROJECT_NAME))
    sudo('sudo a2ensite {}.conf'.format(PROJECT_NAME))


def _make_virtualhost_forhttps():
    script = """'<VirtualHost *:80>
    ServerName {servername}
    <Directory /home/{username}/{project_name}/{project_name}>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIScriptAlias / /home/{username}/{project_name}/{project_name}/wsgi.py
    
    Redirect permanent / https://sayproject.site/
    
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    </VirtualHost>'""".format(
        static_root=STATIC_ROOT_NAME,
        username=env.user,
        project_name=PROJECT_NAME,
        static_url=STATIC_URL_NAME,
        servername=REMOTE_HOST,
        media_url=MEDIA_ROOT
    )
    sudo('echo {} > /etc/apache2/sites-available/{}.conf'.format(script, PROJECT_NAME))
    sudo('sudo a2ensite {}.conf'.format(PROJECT_NAME))


def _make_virtualhost_https():
    script = """'    
    <VirtualHost *:443>
    ServerName {servername}
    Alias /{static_url} /home/{username}/{project_name}/{static_root}
    Alias /{media_url} /home/{username}/{project_name}/{media_url}
    <Directory /home/{username}/{project_name}/{media_url}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{static_root}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{project_name}>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/{servername}/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/{servername}/privkey.pem
    
    WSGIDaemonProcess {project_name} python-home=/home/{username}/.virtualenvs/{project_name} python-path=/home/{username}/{project_name}
    WSGIProcessGroup {project_name}
    WSGIScriptAlias / /home/{username}/{project_name}/{project_name}/wsgi.py
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    </VirtualHost>'""".format(
        static_root=STATIC_ROOT_NAME,
        username=env.user,
        project_name=PROJECT_NAME,
        static_url=STATIC_URL_NAME,
        servername=REMOTE_HOST,
        media_url=MEDIA_ROOT
    )
    sudo('echo {} > /etc/apache2/sites-available/{}.conf'.format(script, PROJECT_NAME+'_https'))
    sudo('sudo a2ensite {}.conf'.format(PROJECT_NAME+'_https'))


def _grant_apache2():
    sudo('sudo chown -R :www-data ~/{}'.format(PROJECT_NAME))


def _grant_sqlite3():
    sudo('sudo chmod 775 ~/{}/db.sqlite3'.format(PROJECT_NAME))


def _grant_ssl_live():
    sudo('sudo chmod 775 /etc/letsencrypt/live'.format(PROJECT_NAME))


def _restart_apache2():
    sudo('sudo service apache2 restart')


def _setup_for_ssl():
    sudo('sudo a2enmod ssl')
    sudo('sudo service apache2 restart')


def apache_stop():
    sudo('sudo service apache2 stop')


def apache_start():
    sudo('sudo service apache2 start')


def _create_superuser_django():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py migrate --noinput' % (
        project_folder, virtualenv_folder
    ))