"""Perform data migrations."""

import optparse
import os
from datetime import datetime

DEFAULT_MIGRATION_PATH = "migrations"
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


def main():
    parser = optparse.OptionParser(description="Run data migrations.")
    parser.add_option(
        "-p", "--path", dest="path", default=DEFAULT_MIGRATION_PATH,
        help="Path to the migrations.")
    parser.add_option(
        "-d", "--description", dest="description", default="new_migration",
        help="Description of the migration to generate.")
    opts, args = parser.parse_args()

    if opts.new_migration:
        _generate_migration(opts.path, opts.description)


def _generate_migration(path, description):

    version = datetime.today().strftime("%Y%m%d%H%M%S")
    base_name = "migration_{0}_{1}".format(version, description.lower())
    name = "{0}/{1}.py".format(path, base_name)
    test_path = os.path.abspath(os.path.join(path, '..', 'tests'))

    test_name = "{0}/migrations/test_{1}.py".format(test_path, base_name)

    if os.path.isdir(os.path.join(path)) == False:
        os.mkdir(os.path.join(path))

    if os.path.isdir(os.path.join(test_path, path)) == False:
        print os.path.join(test_path, path)
        os.mkdir(os.path.join(test_path, path))

    # with open(name, "w") as migration_file:
    #     migration_file.write(MIGRATION_TEMPLATE)

    # print " ".join(("Migration:\n", name, "created!"))

    # with open(test_name, "w") as migration_file:
    #     migration_file.write(MIGRATION_TEST_TEMPLATE.format(base_name))
    # print " ".join(("Test:\n", test_name, "created!"))


if __name__ == "__main__":
    main()
