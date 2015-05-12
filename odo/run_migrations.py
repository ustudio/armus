import os
import re
import importlib
from exceptions import RuntimeError


class MigrationError(RuntimeError):
    pass


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


def _run_migrations(path, migrations, **kwargs):
    for migration in migrations:
        module = _import_module(path, migration)
        module.up(kwargs)


def revert_last_migration(path, migrations):
    migration = sorted(migrations)[-1]
    module = _import_module(path, migration)
    try:
        module.down()
        return migration
    except:
        raise RuntimeError


def apply_new_migrations(path, applied_migrations, **kwargs):
    # path = args[0]
    # applied_migrations = args[1]
    new_migrations = _find_unapplied_migrations(path, applied_migrations)
    _run_migrations(path, new_migrations, **kwargs)
    return new_migrations
