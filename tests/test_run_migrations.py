import unittest
import os

from mock import patch, MagicMock

from odo.run_migrations import DuplicateMigrationVersion
from odo.run_migrations import extract_version, get_migration_versions, build_module_names, find_unapplied_migrations, \
    run_migrations, apply_new_migrations


class TestCreateMigrationFiles(unittest.TestCase):

        def test_extract_version(self):
            test_filename = "migration_20121016152357_first_thing"

            result = extract_version(test_filename)
            self.assertEqual(20121016152357, result)

        def test_get_migration_versions(self):

            test_directory_listing = [
                "migration_20121016152357_first_thing.py",
                "migration_20121016182212_second_thing.py",
                "im_not_a_migration_file.py"
            ]

            with patch('os.listdir', MagicMock(spec=os.listdir)) as mocklistdir:
                mocklistdir.return_value = test_directory_listing
                result = get_migration_versions("some_path")

            self.assertEqual([20121016152357, 20121016182212], result)

        def test_get_migration_versions_disallows_duplicates(self):
            test_directory_listing = [
                "migration_20121016152357_first_thing.py",
                "migration_20121016182212_second_thing.py",
                "migration_20121016182212_other_second_thing.py",
                "im_not_a_migration_file.py"
            ]

            with patch('os.listdir', MagicMock(spec=os.listdir)) as mocklistdir:
                mocklistdir.return_value = test_directory_listing
                with self.assertRaises(DuplicateMigrationVersion):
                    get_migration_versions("some_path")

        def test_build_module_names(self):
            test_directory_listing = [
                "migration_20121016152357_first_thing.py",
                "migration_20121016182212_second_thing.py",
                "im_not_a_migration_file.py"
            ]

            with patch('os.listdir', MagicMock(spec=os.listdir)) as mocklistdir:
                mocklistdir.return_value = test_directory_listing
                result = build_module_names("some_path", [20121016152357, 20121016182212])

            self.assertEqual(
                ["migration_20121016152357_first_thing", "migration_20121016182212_second_thing"],
                result
            )

        def test_find_unapplied_migrations(self):
            no_applied_migrations = []
            one_applied_migration = [20121016152357]
            all_migrations_applied = [20121016152357, 20121016182212]

            test_directory_listing = [
                "migration_20121016182212_second_thing.py",
                "migration_20121016152357_first_thing.py",
                "im_not_a_migration_file.py"
            ]

            with patch('os.listdir', MagicMock(spec=os.listdir)) as mocklistdir:
                mocklistdir.return_value = test_directory_listing
                no_applied_migrations_result = find_unapplied_migrations("some_path", no_applied_migrations)
                one_applied_migration_result = find_unapplied_migrations("some_path", one_applied_migration)
                all_migrations_applied_result = find_unapplied_migrations("some_path", all_migrations_applied)

            self.assertEqual(
                ["migration_20121016152357_first_thing", "migration_20121016182212_second_thing"],
                no_applied_migrations_result
            )

            self.assertEqual(
                ["migration_20121016182212_second_thing"],
                one_applied_migration_result
            )

            self.assertEqual([], all_migrations_applied_result)

        # def test_import_module(self):
        #     # TODO is this testing anything?
        #     with patch('importlib.import_module', MagicMock(spec=importlib.import_module)) as mockimportmodule:
        #         mockimportmodule.return_value = some_module
        #         module = import_module("this/is/a/path", "some_module_name")
        #
        #         self.assertEqual(some_module, module)

        def test_run_migrations(self):
            some_module = MagicMock()
            no_migrations = []
            single_migration = [some_module]
            multiple_migrations = [
                some_module,
                some_module
            ]

            run_migrations(no_migrations)
            self.assertEqual(0, some_module.up.call_count)
            some_module.reset_mock()

            run_migrations(single_migration)
            self.assertEqual(1, some_module.up.call_count)
            some_module.reset_mock()

            run_migrations(multiple_migrations)
            self.assertEqual(2, some_module.up.call_count)
            some_module.reset_mock()

        def test_apply_new_migrations(self):
            # this list comes from the database
            applied_migrations = []
            test_directory_listing = [
                "migration_20121016182212_second_thing.py",
                "migration_20121016152357_first_thing.py",
                "im_not_a_migration_file.py"
            ]

            with patch('os.listdir', MagicMock(spec=os.listdir)) as mocklistdir:
                with patch('odo.run_migrations.run_migrations', MagicMock(spec=run_migrations)) as mockrunmigrations:
                    mocklistdir.return_value = test_directory_listing
                    apply_new_migrations("some_path", applied_migrations)
                    mockrunmigrations.assert_called_with([
                        "migration_20121016152357_first_thing",
                        "migration_20121016182212_second_thing"
                    ])
