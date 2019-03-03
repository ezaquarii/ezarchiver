import unittest as _unittest


class BaseTest(_unittest.TestCase):

    @staticmethod
    def get_fixture_file(filename):
        from os.path import abspath, join, dirname, exists
        fixture_dir = dirname(__file__)
        fixture_file = abspath(join(fixture_dir, 'fixtures', filename))
        if not exists(fixture_file):
            raise RuntimeError("File or directory {file} does not exist".format(file=fixture_file))
        return fixture_file
