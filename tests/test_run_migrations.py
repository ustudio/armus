import unittest
import os
from mock import patch, MagicMock

from odo.run_migrations import extract_version, get_migration_versions


class TestCreateMigrationFiles(unittest.TestCase):

        def test_extract_version(self):
            test_filename = "migration_20121016152357_first_thing"

            result = extract_version(test_filename)
            self.assertEqual(20121016152357, result)

        def test_get_migration_versions(self):

            test_directory_listing = [
                "migration_20121016152357_first_thing",
                "migration_20121016182212_second_thing",
                "im_not_a_migration_file"
            ]

            with patch('os.listdir', MagicMock(spec=os.listdir)) as mocklistdir:
                mocklistdir.return_value = test_directory_listing
                result = get_migration_versions("some_path")

            self.assertEqual([20121016152357, 20121016182212], result)
