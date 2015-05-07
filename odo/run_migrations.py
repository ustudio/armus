import os
import re
import importlib

migration_filter = re.compile('migration_[0-9]{14}.*')


class DuplicateMigrationVersion(Exception):
    pass


def extract_version(name):
    try:
        version = int(name.split("_")[1])
        return version
    # TODO make this more accurate
    except ValueError:
        return None


def get_migration_versions(path):
    versions = []
    migration_files = [filename for filename in os.listdir(path) if migration_filter.match(filename)]

    for migration_file in migration_files:
        version = extract_version(migration_file)
        if version in versions:
            message = "Duplicate migration version in migration file list"
            raise DuplicateMigrationVersion(message)
        else:
            versions.append(version)

    return sorted(versions)


def build_module_names(path, versions):
    migration_files = [filename for filename in os.listdir(path) if migration_filter.match(filename)]

    module_names = []
    for filename in migration_files:
        version = extract_version(filename)
        if version and version in versions:
            module_names.append(os.path.splitext(filename)[0])

    return sorted(module_names, key=str.lower)


def find_unapplied_migrations(path, applied_versions):
    all_migration_versions = get_migration_versions(path)
    new_migration_versions = [
        version for version in all_migration_versions if version not in applied_versions
    ]

    migration_module_names = build_module_names(path, new_migration_versions)

    return migration_module_names


def import_module(path, module_name):
    package_name = os.path.basename(path)
    module = importlib.import_module(package_name + "." + module_name)
    return module


def run_migrations(migrations):
    for migration in migrations:
        migration.up()

# TODO revert_last_migration


def apply_new_migrations(path, applied_migrations):
    new_migrations = find_unapplied_migrations(path, applied_migrations)
    run_migrations(new_migrations)
