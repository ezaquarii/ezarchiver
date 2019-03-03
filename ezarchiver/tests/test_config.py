from os.path import join, abspath, dirname

from ezarchiver.tests import BaseTest
from ezarchiver import Config


class TestLoadConfig(BaseTest):

    @staticmethod
    def load_fixture_config(filename):
        config_file = TestLoadConfig.get_fixture_file(filename)
        return Config(config_file), config_file

    def test_root_is_loaded_from_config(self):
        config, _ = self.load_fixture_config('configs/with_root')
        self.assertEqual(config.root, '/test/root')

    def test_root_is_derived_from_config_location(self):
        config, config_file = self.load_fixture_config('configs/without_root')
        self.assertEqual(config.root, dirname(config_file))

    def test_include_exclude_are_optional(self):
        config, _ = self.load_fixture_config('configs/no_include_no_exclude')
        self.assertEqual(config.include, [])
        self.assertEqual(config.exclude, [])


class TestLoadConfigFromDirectory(BaseTest):

    @staticmethod
    def load_fixture_config(filename):
        config_file = TestLoadConfig.get_fixture_file(filename)
        return Config(config_file), config_file

    def test_load_valid_config(self):
        config, config_file = self.load_fixture_config('directories/valid')
        self.assertEqual(config.root, self.get_fixture_file('directories/valid'))

    def test_load_config_with_explicit_root(self):
        with self.assertRaises(ValueError):
            self.load_fixture_config('directories/invalid_with_root')

    def test_load_config_from_directory_without_config_file(self):
        with self.assertRaises(ValueError):
            self.load_fixture_config('directories/invalid_no_config_file')
