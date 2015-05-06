"""Module containg data migration utilities.

1. Add a file named <version>_<description>.py to migrations/
2. Define a Migration class in this file. This class must accept a version
number as initialization parameter.

"""

import abc
# import os
# import sys
# import time

# import mogo


# class MigrationVersion(mogo.Model):
#     version = mogo.Field(int, required=True)
#     created = mogo.Field(float, required=True)

#     @classmethod
#     def new(cls, version, created):
#         return MigrationVersion(version=version, created=created)


class MigrationBase(object):
    __meta__ = abc.ABCMeta

    def __init__(self, version):
        self.version = int(version)

    @abc.abstractmethod
    def up(self, logger):
        """The up method to perform the data changes required by the migration.

        """
        pass

    @abc.abstractmethod
    def down(self, logger):
        """The down method should reverse the effects if the up method."""
        pass


def run_migrations(path, logger):
    pass
    # # FTF - Strategy to determine what has been applied (DB abstraction).
    # # make sure it's an absolute path
    # path = os.path.abspath(path)

    # # make sure we weren't passed a file
    # assert os.path.isdir(path)

    # logger.info("Fetching applied migrations.")

    # applied_versions = frozenset(
    #     [migration.version for migration in MigrationVersion.find()])

    # logger.info("Found (%s) applied migrations.", len(applied_versions))
    # logger.debug("Applied versions are (%s).", applied_versions)

    # migration_module_names = _find_unapplied_migrations(
    #     path, applied_versions, logger)

    # logger.info(
    #     "Unapplied migrations in (%s) are (%s).", path, migration_module_names)

    # if len(migration_module_names) == 0:
    #     logger.debug("No new migrations found.")
    #     return

    # migrations = _create_migrations(path, migration_module_names, logger)
    # logger.debug("Running migrations.")

    # _run(migrations, logger)


# def revert_last(path, logger):
#     logger.info("Reverting last run migrations.")

#     migrations_in_reverse = MigrationVersion.find().order(created=mogo.DESC)
#     if 0 == migrations_in_reverse.count():
#         logger.info("No migrations to revert.")
#         return

#     migration_version_to_revert = migrations_in_reverse[0]

#     logger.info(
#         "Reverting version (%s) with timestamp (%s).",
#         migration_version_to_revert.version,
#         migration_version_to_revert.created)

#     module_name = _build_module_names(
#         path, [migration_version_to_revert.version], logger)

#     logger.info("Reverting module (%s).", module_name[0])

#     MigrationClass = _import_name(path, module_name[0], "Migration", logger)
#     migration = MigrationClass(migration_version_to_revert.version)
#     migration.down(logger)
#     MigrationVersion.remove({
#         "version": migration.version
#     })


# def _create_migrations(path, module_names, logger):
#     migrations = []
#     for module_name in module_names:
#         version = _extract_version(module_name)
#         if not version:
#             raise ValueError(
#                 "Invalid module name (%s). An underscored version prefix is "
#                 "required.", module_name)

#         logger.debug("Importing migration from version (%s).", version)

#         MigrationClass = _import_name(
#             path, module_name, "Migration", logger)

#         migration = MigrationClass(version)
#         migrations.append(migration)

#     return migrations


# def _find_unapplied_migrations(path, applied, logger):
#     all = _all_versions(path)
#     logger.debug("All versions are (%s).", all)
#     new = all.difference(applied)
#     logger.debug("New versions are (%s).", new)
#     migration_module_names = _build_module_names(path, new, logger)
#     sorted_names = sorted(migration_module_names, key=str.lower)
#     return sorted_names


# # How to handle failed migrations? e.g. 1 succedes, 2 fails, do you run 3?
# def _run(migrations, logger):
#     for migration in migrations:
#         logger.info("Running migration (%s).", migration.__module__)
#         migration.up(logger)
#         MigrationVersion.create(
#             version=migration.version, created=time.time())


# def _import_name(package_path, module_name, name, logger):
#     base_path = os.path.dirname(package_path)
#     if base_path not in sys.path:
#         logger.debug("Adding path '%s' to sys.path.", base_path)
#         sys.path.insert(0, base_path)
#     package_name = os.path.basename(package_path)

#     if not package_name.endswith("."):
#         package_name += "."

#     logger.debug(
#         "Import (%s) from module (%s%s).", name, package_name, module_name)
#     try:
#         package = __import__("%s%s" % (package_name, module_name))
#         module = getattr(package, module_name)
#     except ImportError as error:
#         logger.warning(
#             "Unable to import module (%s). Name (%s) not imported. Error: %s",
#             module_name, name, error)
#         raise
#     return getattr(module, name)


# def _all_versions(path):
#     versions = set()
#     for directory_info in os.walk(path):
#         # tuple index 2 is the list of filenames
#         for filename in directory_info[2]:
#             version = _extract_version(filename)
#             if version:
#                 versions.add(version)
#     return versions


# def _build_module_names(path, versions, logger):
#     logger.debug("Building module names from versions (%s)." % (versions))

#     module_names = []
#     for directory_info in os.walk(path):
#         for filename in directory_info[2]:
#             extension = filename.rsplit(".", 1)[-1]
#             if not extension or extension != "py":
#                 continue

#             logger.debug(
#                 "Checking for migration module in file (%s).", filename)

#             version = _extract_version(filename)
#             if version and version in versions:
#                 module_names.append(filename.rsplit(".", 1)[0])

#     return module_names


# def _extract_version(name):
#     try:
#         version = int(name.split("_")[1])
#         return version
#     except ValueError:
#         return None
#     raise


# class MigrationError(StandardError):
#     """Helper error for migrations to use."""
#     pass
