import argparse
from ezarchiver import Config, Duplicity

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EZ Archiver')
    parser.add_argument('type', metavar='TYPE', help='Type of backup, either full or incr')
    parser.add_argument('config', metavar="ARCHIVEFILE", help='Backup job configuration file')
    parser.add_argument('--allow-source-mismatch', action='store_true', help='Allow performing backup with changed source directory')

    arguments = parser.parse_args()

    config = Config(arguments.config)
    duplicity = Duplicity(config, arguments.type)

    duplicity.backup(allow_source_mismatch=arguments.allow_source_mismatch)
