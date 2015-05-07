"""Perform data migrations."""

import logging
import optparse
import os
from datetime import datetime

DEFAULT_MIGRATION_PATH = "migrations"
VERSION_FORMAT = "%Y%m%d%H%M%S"
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

from migrations.%(migration_basename)s import Migration

from tests.helpers import database_connection
from tests.helpers import factories


class TestMigration(database_connection.MongoConnectionTestCase):
    def test_new_migration(self):
        migration = Migration(%(migration_version)s)


        migration.up(logger)
        migration.down(logger)

        self.assertTrue(False, "Migration test has not been written yet.")
"""


def main():
    logger = logging.getLogger("migrate")
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    parser = optparse.OptionParser(description="Run data migrations.")
    parser.add_option(
        "-p", "--path", dest="path", default=DEFAULT_MIGRATION_PATH,
        help="Path to the migrations.")
    parser.add_option(
        "-n", "--new-migration", action="store_true", dest="new_migration",
        default=False, help="Generate a new migration file.")
    parser.add_option(
        "-d", "--description", dest="description", default="new_migration",
        help="Description of the migration to generate.")
    opts, args = parser.parse_args()

    if opts.new_migration:
        _generate_migration(opts.path, opts.description, logger)


def _generate_migration(path, description, logger):

    version = datetime.today().strftime("%Y%m%d%H%M%S")
    base_name = "migration_{0}_{1}".format(version, description.lower())
    name = "{0}/{1}.py".format(path, base_name)
    test_path = os.path.abspath(os.path.join(path, '..', 'tests'))
    test_name = "{0}/migrations/test_{1}.py".format(test_path, base_name)

    logger.info("Generating new migration file ({0}).".format(name))

    with open(name, "w") as file:
        file.write(MIGRATION_TEMPLATE)

    logger.info("Generating new migration test ({0}).".format(test_name))

    with open(test_name, "w") as file:
        file.write(MIGRATION_TEST_TEMPLATE % {
            "migration_basename": base_name,
            "migration_version": version
        })


if __name__ == "__main__":
    main()
