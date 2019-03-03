#!env/bin/python

from os.path import join, abspath
import subprocess


class Duplicity(object):

    def __init__(self, config, type=None):
        self.config = config
        self.type = type

    @staticmethod
    def _build_exclude_params(root, excludes):
        params = []
        for item in excludes:
            params.append('--exclude')
            params.append(abspath(join(root, item)))
        return params

    @staticmethod
    def _build_include_params(root, includes):
        params = []
        for item in includes:
            params.append('--include')
            params.append(abspath(join(root, item)))
        return params

    @staticmethod
    def _build_b2_destination_path(bucket, folder):
        from os.path import relpath, join, normpath, isabs, split
        normalized_folder = normpath(relpath(folder, '/') if isabs(folder) else folder)
        destination = normpath(join(bucket, normalized_folder))
        if not destination.startswith(bucket):
            raise ValueError("[%s]: your folder should be inside bucket." % folder)
        else:
            return destination

    @staticmethod
    def _build_b2_destination_auth(account_id, application_key=None):
        if application_key:
            return "{account_id}:{application_key}".format(account_id=account_id, application_key=application_key)
        else:
            return "{account_id}".format(account_id=account_id)

    @staticmethod
    def _build_b2_destination(b2_config):
        return "b2://{auth}@{path}".format(
            auth=Duplicity._build_b2_destination_auth(b2_config['account_id'], b2_config.get('application_key', None)),
            path=Duplicity._build_b2_destination_path(b2_config['bucket'], b2_config.get('folder', '/'))
        )

    def flatten(self, l):
        """
        Flatten list containing nested lists. None are filtered out.
        """
        out = []
        for i in l:
            if isinstance(i, list):
                out.extend(i)
            elif i is not None:
                out.append(i)
        return out

    def backup(self, allow_source_mismatch):
        """
        Archive directories according to loaded config.

        :param allow_source_mismatch: Pass --allow-source-mismatch to duplicity, if you changed the backup root directory
        """
        import subprocess

        cmd = self.flatten([
            'duplicity',
            self.type,
            '--allow-source-mismatch' if allow_source_mismatch else None,
            '--progress',
            ['--encrypt-key', self.config.gpg_key_id],
            self._build_include_params(self.config.root, self.config.include),
            self._build_exclude_params(self.config.root, self.config.exclude),
            self.config.root,
            self._build_b2_destination(self.config.b2)
        ])

        subprocess.call(cmd)

    def restore(self, destination):
        """
        Restore backup into a given destination directory.
        If directory does not exist, it will be created.
        If directory exists but is not empty, backup will be aborted to avoid unexpected overwrites.

        :param destination: Destination directory.
        :return:
        """
        cmd = self.flatten([
            'duplicity',
            'restore',
            self._build_b2_destination(self.config.b2),
            destination
        ])

        subprocess.call(cmd)
