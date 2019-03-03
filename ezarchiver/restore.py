import argparse
from ezarchiver import Config, Duplicity

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EZ Archiver')
    parser.add_argument('config', metavar="ARCHIVEFILE", help='Backup job configuration file')
    parser.add_argument('destination', metavar='DESTINATION', help='Destination directory')

    arguments = parser.parse_args()

    config = Config(arguments.config)
    duplicity = Duplicity(config)

    duplicity.restore(arguments.destination)
