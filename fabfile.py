from fabric.api import *
from fabric.colors import *
import fabric.state
# fabric.state.output['debug'] = False
# fabric.state.output['status'] = False
# fabric.state.output['warnings'] = False
fabric.state.output['running'] = False
# fabric.state.output['user'] = False
# fabric.state.output['stderr'] = False
# fabric.state.output['aborts'] = False

# fab project_name:magic,True create_basic_django_project create_gitignore add_gunicorn_to_settings add_django_extensions_to_settings add_django_debug_toolbar_to_settings


def project_name(project_name='testing', debug='false'):
    """
    Sets the project_name to be used at the script execution.
    """
    env.project_name = project_name
    env.debug = debug.lower() == 'true'
    print(green("Project Name: {project_name}".format(**env), bold=True))
    if env.debug:
        print(green("DEBUG MODE ON", bold=True))


def create_basic_django_project():
    """
    Creates a basic Django project.
    """
    command = """
    mkdir {project_name}
    cd {project_name}
    virtualenv --no-site-packages .
    source bin/activate
    pip install ../Django-1.3.1.tar.gz
    django-admin.py startproject {project_name}
    cd {project_name}
    chmod 755 manage.py
    ./manage.py startapp main
    cat > requirements.txt <<EOF
django==1.3.1
EOF
    cat > dev-requirements.txt <<EOF
-r requirements.txt
EOF
    """.format(**env)
    local(command, capture=not env.debug)


def install_dev_requirements():
    """
    Install dev-requirements file
    """
    command = """
    cd {project_name}/{project_name}
    source bin/activate
    pip install -r dev-requirements.pip
    """.format(**env)
    local(command, capture=not env.debug)


def install_requirements():
    """
    Install dev-requirements file
    """
    command = """
    cd {project_name}/{project_name}
    source bin/activate
    pip install -r requirements.pip
    """.format(**env)
    local(command, capture=not env.debug)


def create_gitignore():
    """
    Creates the basic .gitignore file.
    """
    command = """
    cd {project_name}
    cat > .gitignore <<EOF
# Virtualenv
/bin
/lib
/include
/build
/src
.Python

# Python
*.pyc

# Dev
db.sqlite

# Eclipse/Aptana/PyDev
.project
.pydevproject

# Misc
.DS_Store
EOF
    """.format(**env)
    local(command, capture=not env.debug)


def setup_heroku():
    """
    Sets up Heroku, this must be run on a initializated git repo.
    """
    command = """
    cd {project_name}
    heroku create --stack cedar
    cat > Procfile <<EOF
web: bin/python {project_name}/manage.py run_gunicorn -b 0.0.0.0:\$PORT -w 3
EOF
    cat > requirements.txt <<EOF
psycopg==2.4.2
gunicorn==0.13.4
-r {project_name}/requirements.txt
EOF
    """.format(**env)
    local(command, capture=not env.debug)


def add_gunicorn_to_settings():
    """
    Adds gunicorn to our Django settings.py file.
    """
    command = """
    cd {project_name}
    cat >> {project_name}/settings.py <<EOF

# Magic import: if gunicorn is available add it to our INSTALLED_APPS
try:
    import gunicorn
    INSTALLED_APPS += ('gunicorn',)
except ImportError:
    pass
EOF
    """.format(**env)
    local(command, capture=not env.debug)


def add_django_extensions_to_settings():
    """
    Installs and adds django-extensions to our Django settings.py file.
    """
    command = """
    cd {project_name}
    cat >> {project_name}/dev-requirements.txt <<EOF
django-extensions==0.7.1
EOF
    cat >> {project_name}/settings.py <<EOF

# Magic import: if django_extensions is available add it to our INSTALLED_APPS
try:
    import django_extensions
    INSTALLED_APPS += ('django_extensions',)
except ImportError:
    pass
EOF
    """.format(**env)
    local(command, capture=not env.debug)


def add_django_debug_toolbar_to_settings():
    """
    Installs and adds django-debug-toolbar to our Django settings.py file.
    """
    command = """
    cd {project_name}
    cat >> {project_name}/dev-requirements.txt <<EOF
django-debug-toolbar==0.9.1
EOF
    cat >> {project_name}/settings.py <<EOF

# Magic import: if debug_toolbar is available add it to our INSTALLED_APPS
try:
    import debug_toolbar
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {{
        'INTERCEPT_REDIRECTS': False,
    }}
except ImportError:
    pass
EOF
    """.format(**env)
    local(command, capture=not env.debug)