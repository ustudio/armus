import os
import re
import importlib


migration_filter = re.compile(r"^migration_\d+.*\.py$")


def _get_migration_versions(path):
    migration_files = [
        filename for filename in os.listdir(path) if migration_filter.match(filename)
    ]
    return sorted(migration_files)


def _find_unapplied_migrations(path, applied_migrations):
    all_migrations = _get_migration_versions(path)
    new_migrations = [
        os.path.splitext(migration)[0] for migration in all_migrations if migration not in applied_migrations
    ]

    return new_migrations


def _import_module(path, module_name):
    package_name = os.path.basename(path)
    module = importlib.import_module(package_name + "." + module_name)
    return module


def _run_migrations(path, migrations):
    for migration in migrations:
        module = _import_module(path, migration)
        module.up()

# TODO revert_last_migration


def apply_new_migrations(path, applied_migrations):
    new_migrations = _find_unapplied_migrations(path, applied_migrations)
    _run_migrations(path, new_migrations)
    return new_migrations

