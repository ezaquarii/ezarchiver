import os.path

from ezarchiver.tests import BaseTest
from ezarchiver.duplicity import Duplicity


class TestBuildParams(BaseTest):

    def test_build_exclude_params(self):
        params = Duplicity._build_exclude_params('/root', ['1', '2'])
        self.assertEqual(['--exclude', '/root/1', '--exclude', '/root/2'], params)

    def test_build_include_params(self):
        params = Duplicity._build_include_params('/root', ['1', '2'])
        self.assertEqual(['--include', '/root/1', '--include', '/root/2'], params)

    def test_build_b2_destination_path(self):
        fixture = [
            dict(bucket='bucket', folder='',               expected='bucket'),
            dict(bucket='bucket', folder='/',              expected='bucket'),
            dict(bucket='bucket', folder='/dir',           expected='bucket/dir'),
            dict(bucket='bucket', folder='/dir/..',        expected='bucket'),
            dict(bucket='bucket', folder='dir',            expected='bucket/dir'),
            dict(bucket='bucket', folder='dir/..',         expected='bucket'),
            dict(bucket='bucket', folder='dir/subdir',     expected='bucket/dir/subdir'),
            dict(bucket='bucket', folder='/dir/subdir',    expected='bucket/dir/subdir'),
            dict(bucket='bucket', folder='./dir/./subdir', expected='bucket/dir/subdir'),
            dict(bucket='bucket', folder='./dir/../subdir', expected='bucket/subdir')
        ]
        for f in fixture:
            self.assertEqual(Duplicity._build_b2_destination_path(f['bucket'], f['folder']), f['expected'])

    def test_build_b2_destination_path_outside_bucket(self):
        folders = [
            '../folder',
            'folder/../..'
        ]
        for folder in folders:
            with self.assertRaises(ValueError):
                Duplicity._build_b2_destination_path('bucket', folder)

    def test_build_b2_destination_auth_with_application_key(self):
        auth = Duplicity._build_b2_destination_auth(account_id='id', application_key='key')
        self.assertEqual('id:key', auth)

    def test_build_b2_destination_auth_without_application_key(self):
        auth = Duplicity._build_b2_destination_auth(account_id='id', application_key=None)
        self.assertEqual('id', auth)

    def test_destination_with_application_key(self):
        b2_config = {
            'account_id': 'test_account_id',
            'application_key': 'test_application_id',
            'bucket': 'test_bucket',
            'folder': '/'
        }
        param = Duplicity._build_b2_destination(b2_config)
        self.assertEqual('b2://test_account_id:test_application_id@test_bucket', param)

    def test_destination_without_application_key(self):
        b2_config = {
            'account_id': 'test_account_id',
            'bucket': 'test_bucket',
            'folder': '/'
        }
        param = Duplicity._build_b2_destination(b2_config)
        self.assertEqual('b2://test_account_id@test_bucket', param)
