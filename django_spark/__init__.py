VERSION = (0, 0, 1)

def get_version():
   return '%s.%s.%s' % VERSION

version = get_version()

import sys
import os

def main():
    from fabric.main import main as main_fabric
    file_name = os.path.join(os.path.dirname( __file__ ), 'fabfile.py')
    sys.argv = sys.argv[0:1] + ['-f', file_name] + sys.argv[1:]
    main_fabric()