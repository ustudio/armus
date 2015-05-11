import tempfile
from bin import create_migration
import os
import unittest
import shutil
from datetime import datetime
from mock import patch
import optparse
from collections import namedtuple

VERSION_FORMAT = "%Y%m%d%H%M%S"
MIGRATION_TEMPLATE = """
def up():
    pass


def down():
    pass
"""

MIGRATION_TEST_TEMPLATE = """
\"\"\"(Write a doc string).\"\"\"
import unittest
from migrations import {0}


class TestMigration(unittest.TestCase):
    def test_new_migration(self):
        migration = {0}

        migration.up()
        migration.down()

        self.assertTrue(False, "Migration test has not been written yet.")
"""


class TestCreateMigrationFiles(unittest.TestCase):

    @patch('optparse.OptionParser.parse_args')
    def test_create_migration_files(self, mock_parse_args):
        description = "fake_description"
        version = datetime.today().strftime(VERSION_FORMAT)

        base_name = "migration_{0}_{1}".format(version, description.lower())

        base_dir = tempfile.mkdtemp()
        os.mkdir(base_dir + "/migrations")
        os.mkdir(base_dir + "/tests")
        os.mkdir(base_dir + "/tests/migrations")

        command_line_args = namedtuple('literal', 'path new_migration description')(
            path=base_dir + "/migrations", new_migration=True, description=description)
        mock_parse_args.return_value = (command_line_args, [])

        create_migration.main()

        self.assertTrue(os.path.exists(base_dir + "/migrations/" + base_name + ".py"))
        self.assertTrue(os.path.exists(base_dir + "/tests/migrations/test_" + base_name + ".py"))
        self.assertEqual(
            MIGRATION_TEMPLATE, open(base_dir + "/migrations/" + base_name + ".py", "r").read())
        self.assertEqual(
            MIGRATION_TEST_TEMPLATE.format(base_name),
            open(base_dir + "/tests/migrations/test_" + base_name + ".py", "r").read()
        )

        shutil.rmtree(base_dir)
