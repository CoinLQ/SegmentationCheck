#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join
from fabric.api import env, task
from fagungis.tasks import *


@task
def segmentation_check():
    #  name of your project - no spaces, no special chars
    env.project = 'segmentation_check'
    #  hg repository of your project
    env.repository = 'git@github.com:CoinLQ/SegmentationCheck.git'
    #  hosts to deploy your project, users must be sudoers
    env.hosts = ['root@112.74.23.141', ]
    # additional packages to be installed on the server
    env.additional_packages = [
        'mercurial',
    ]
    #  system user, owner of the processes and code on your server
    #  the user and it's home dir will be created if not present
    env.django_user = 'django'
    # user group
    env.django_user_group = env.django_user
    #  the code of your project will be located here
    env.django_user_home = join('/opt', env.django_user)
    #  projects path
    env.projects_path = join(env.django_user_home, 'projects')
    #  the root path of your project
    env.code_root = join(env.projects_path, env.project)
    #  the path where manage.py of this project is located
    env.django_project_root = env.code_root
    #  the Python path to a Django settings module.
    env.django_project_settings = 'settings'
    #  django media dir
    env.django_media_path = join(env.code_root, 'media')
    #  django static dir
    env.django_static_path = join(env.code_root, 'static')
    #  django media url and root dir
    env.django_media_url = '/site_media/media/'
    env.django_media_root = env.code_root
    #  django static url and root dir
    env.django_static_url = '/site_media/static/'
    #env.django_static_root = env.code_root
    env.django_static_root = join(env.code_root, 'static')
    #  do you use south in your django project?
    env.south_used = False
    #  virtualenv root
    env.virtenv = join(env.django_user_home, 'envs', env.project)
    #  some virtualenv options, must have at least one
    env.virtenv_options = ['distribute', 'no-site-packages', ]
    #  location of your pip requirements file
    #  http://www.pip-installer.org/en/latest/requirements.html#the-requirements-file-format
    #  set it to None to not use
    env.requirements_file = join(env.code_root, 'requirements.txt')
    #  always ask user for confirmation when run any tasks
    env.ask_confirmation = False

    ### START gunicorn settings ###
    #  be sure to not have anything running on that port
    env.gunicorn_bind = "127.0.0.1:8100"
    env.gunicorn_logfile = '%(django_user_home)s/logs/projects/%(project)s_gunicorn.log' % env
    env.rungunicorn_script = '%(django_user_home)s/scripts/rungunicorn_%(project)s.sh' % env
    env.gunicorn_workers = 2
    env.gunicorn_worker_class = "eventlet"
    env.gunicorn_loglevel = "info"
    ### END gunicorn settings ###

    ### START nginx settings ###
    env.nginx_server_name = '112.74.23.141'  # Only domain name, without 'www' or 'http://'
    env.nginx_conf_file = '%(django_user_home)s/configs/nginx/%(project)s.conf' % env
    env.nginx_client_max_body_size = 10  # Maximum accepted body size of client request, in MB
    env.nginx_htdocs = '%(django_user_home)s/htdocs' % env
    # will configure nginx with ssl on, your certificate must be installed
    # more info here: http://wiki.nginx.org/HttpSslModule
    env.nginx_https = False
    ### END nginx settings ###

    ### START supervisor settings ###
    # http://supervisord.org/configuration.html#program-x-section-settings
    # default: env.project
    env.supervisor_program_name = env.project
    env.supervisorctl = '/usr/bin/supervisorctl'  # supervisorctl script
    env.supervisor_autostart = 'true'  # true or false
    env.supervisor_autorestart = 'true'  # true or false
    env.supervisor_redirect_stderr = 'true'  # true or false
    env.supervisor_stdout_logfile = '%(django_user_home)s/logs/projects/supervisord_%(project)s.log' % env
    env.supervisord_conf_file = '%(django_user_home)s/configs/supervisord/%(project)s.conf' % env
    ### END supervisor settings ###


@task
def deploy():
    #import code; code.interact(local=dict(globals(), **locals()))
    #  test configuration start
    if not test_configuration():
        if not console.confirm("Configuration test %s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")
    #  test configuration end
    _verify_sudo()
    if env.ask_confirmation:
        if not console.confirm("Are you sure you want to deploy in %s?" % red_bg(env.project.upper()), default=False):
            abort("Aborting at user request.")
    puts(green_bg('Start deploy...'))
    start_time = datetime.now()

    hg_pull()
    _install_requirements()
    _prepare_django_project()
    _prepare_media_path()
    _supervisor_restart()

    end_time = datetime.now()
    finish_message = '[%s] Correctly deployed in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)

def _deploy_static():
    with cd(env.code_root):
        run('python manage.py collectstatic -v0 --noinput')

def _verify_sudo():
    ''' we just check if the user is sudoers '''
    sudo('cd .')


def _install_requirements():
    ''' you must have a file called requirements.txt in your project root'''
    if 'requirements_file' in env and env.requirements_file:
        virtenvsudo('pip install -r %s' % env.requirements_file)


def _reload_supervisorctl():
    sudo('%(supervisorctl)s reread' % env)
    sudo('%(supervisorctl)s reload' % env)

def _prepare_django_project():
    with cd(env.django_project_root):
        if env.south_used:
            virtenvrun('python manage.py migrate --noinput --verbosity=1')
        virtenvsudo('python manage.py collectstatic --noinput')

def _prepare_media_path():
    path = env.django_media_path.rstrip('/')
    sudo('mkdir -p %s' % path)
    sudo('chmod -R 775 %s' % path)

def _supervisor_restart():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('%(supervisorctl)s restart %(supervisor_program_name)s' % env)
    if 'ERROR' in res:
        print red_bg("%s NOT STARTED!" % env.supervisor_program_name)
    else:
        print green_bg("%s correctly started!" % env.supervisor_program_name)
