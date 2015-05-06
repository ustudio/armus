import tempfile
import logging
from bin import create_migration
import os
import unittest
import shutil
from odo.utils import date

logger = logging.getLogger("migrate")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

MIGRATION_TEMPLATE = """
from odo.migrations import migrations


class Migration(migrations.MigrationBase):
    def up(self, logger):
        pass

    def down(self, logger):
        pass
"""

MIGRATION_TEST_TEMPLATE = """
\"\"\"(Write a doc string).\"\"\"
import logging as logger

from migrations.{0} import Migration

from tests.helpers import database_connection
from tests.helpers import factories


class TestMigration(database_connection.MongoConnectionTestCase):
    def test_new_migration(self):
        migration = Migration({1})


        migration.up(logger)
        migration.down(logger)

        self.assertTrue(False, "Migration test has not been written yet.")
"""


class TestCreateMigrationFiles(unittest.TestCase):

    def test_create_migration_files(self):
        description = "fake_description"
        version = date.make_timestamp()
        base_name = "_{0}_{1}".format(version, description.lower())

        base_dir = tempfile.mkdtemp()
        os.mkdir(base_dir + "/migrations")
        os.mkdir(base_dir + "/tests")
        os.mkdir(base_dir + "/tests/migrations")
        create_migration._generate_migration(base_dir + "/migrations", description, logger)

        self.assertTrue(os.path.exists(base_dir + "/migrations/" + base_name + ".py"))
        self.assertTrue(os.path.exists(base_dir + "/tests/migrations/test" + base_name + ".py"))
        self.assertEqual(
            MIGRATION_TEMPLATE, open(base_dir + "/migrations/" + base_name + ".py", "r").read())
        self.assertEqual(
            MIGRATION_TEST_TEMPLATE.format(base_name, version),
            open(base_dir + "/tests/migrations/test" + base_name + ".py", "r").read()
        )

        shutil.rmtree(base_dir)

