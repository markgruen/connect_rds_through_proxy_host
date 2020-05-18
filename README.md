# connect_rds_through_proxy_host
connect to an RDS instance through a proxyhost with no passwords in clear text


./secrets_config_editor.py --help
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
