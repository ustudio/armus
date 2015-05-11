import unittest
# import importlib
from mock import patch, MagicMock
from odo.run_migrations import apply_new_migrations


class TestApplyNewMigrations(unittest.TestCase):

        @patch('os.listdir')
        @patch('odo.run_migrations._import_module')
        def test_applies_all_new_migrations(self, mock_import_module, mock_listdir):
            # this list comes from the database
            some_module = MagicMock()
            applied_migrations = []
            test_directory_listing = [
                "migration_20121016182212_second_thing.py",
                "migration_20121016152357_first_thing.py",
                "im_not_a_migration_file.py"
            ]

            mock_listdir.return_value = test_directory_listing
            mock_import_module.return_value = some_module

            migrations_run = apply_new_migrations("this/is/some_path", applied_migrations)

            self.assertEqual([
                "migration_20121016152357_first_thing",
                "migration_20121016182212_second_thing",
            ], migrations_run)
            self.assertEqual(2, mock_import_module.return_value.up.call_count)

        @patch('os.listdir')
        @patch('importlib.import_module')
        def test_applies_some_new_migrations(self, mock_import_module, mock_listdir):
            # this list comes from the database
            applied_migrations = ["migration_20121016152357_first_thing.py"]
            test_directory_listing = [
                "migration_20121016182212_second_thing.py",
                "migration_20121016152357_first_thing.py",
                "im_not_a_migration_file.py"
            ]

            mock_listdir.return_value = test_directory_listing

            migrations_run = apply_new_migrations("this/is/some_path", applied_migrations)

            mock_import_module.assert_called_with('some_path.migration_20121016182212_second_thing')
            self.assertEqual([
                "migration_20121016182212_second_thing",
            ], migrations_run)
            self.assertEqual(1, mock_import_module.return_value.up.call_count)

        @patch('os.listdir')
        @patch('importlib.import_module')
        def test_applies_no_new_migrations(self, mock_import_module, mock_listdir):
            # this list comes from the database
            applied_migrations = [
                "migration_20121016152357_first_thing.py",
                "migration_20121016182212_second_thing.py",
            ]
            test_directory_listing = [
                "migration_20121016182212_second_thing.py",
                "migration_20121016152357_first_thing.py",
                "im_not_a_migration_file.py"
            ]

            mock_listdir.return_value = test_directory_listing

            migrations_run = apply_new_migrations("this/is/some_path", applied_migrations)

            self.assertEqual(0, mock_import_module.call_count)
            self.assertEqual([], migrations_run)
            self.assertEqual(0, mock_import_module.return_value.up.call_count)
