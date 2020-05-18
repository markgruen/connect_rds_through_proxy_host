#!/usr/bin/env python2.7
"""
Secret Config Editor

Used to add encrypted secrets to configuration files.

Usage:
  secret_config_editor.py set --section <SECTION> --config <PATH> --key <KEY_PATH>
  secret_config_editor.py --version
  secret_config_editor.py --help

Options:
  -h --help            Show this screen.
  --version            Show version.
  --section=<SECTION>  Section to add encrypted password.
  --config=<PATH>      Path to config file.
  --key=<KEY_PATH>     Path to key file.

Notes:
   This tool will add an encrypted password attribute to the configuration file. If the 
   key file does exist the tool will create one on the first run.

   I suggest storing keys in your home directory under a hidden directory ~/.keys


Example:

   ./secrets_config_editor.py set --section=uweee_dev --config=~/config.ini --key=~/.keys/db.key

"""

import os
import getpass
from docopt import docopt
from secureconfig import SecureConfigParser, SecureConfigException
try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
    exit('This script requires that `schema` data-validation library'
         ' is installed: \n    pip install schema\n'
         'https://github.com/halst/schema')

_version_ = "0.1.1"

class Error(Exception):
   """Base class for other exceptions"""
   pass


class SectionError(Error):
   """Section doesn't exist"""
   pass


class KeyFileError(Error):
   """Key file path or permissions problems"""
   pass


def open_config(args):
    key_path = os.path.expanduser(args['--key'])
    key_dir = os.path.dirname(key_path)

    if not os.path.exists(key_path):
        import stat
        scfg = SecureConfigParser.from_file(key_path)
        os.chmod(key_path, stat.S_IRUSR)
    else:
        scfg = SecureConfigParser.from_file(key_path)

    scfg.read(args['--config'])
    return scfg


def check_section(args):
    scfg = open_config(args)
    if not scfg.has_section(args['--section']):
        raise SectionError(args['--section'])
    return scfg


def main(args, scfg):

    scfg.set(args['--section'],'dbpassword', getpass.getpass(), encrypt=True)

    fh=open(args['--config'], 'w')
    scfg.write(fh)
    fh.close()


if __name__ == '__main__':
    args = docopt(__doc__, version='Secret Config Editor {}'.format(_version_))
    #print(args)

    schema = Schema({
                '--config': And(Use(os.path.expanduser),os.path.exists,lambda s: os.access(s, os.W_OK), 
                                error='--config={} must be writable'.format(args['--config'])),
                '--key': And(lambda p: os.path.exists(os.path.dirname(os.path.expanduser(p))), 
                            error='--key={} path must exist. \nThe complete key path is {}'.format(
                                                os.path.dirname(os.path.expanduser(args['--key'])),
                                                os.path.expanduser(args['--key']))),
                str: object
    })

    try:
        args = schema.validate(args)
        scfg = check_section(args)
        main(args, scfg)
    except SchemaError as e:
        exit(e)
    except SectionError as se:
        print("Error: Section {} doesn't exist in configuration file".format(se))
