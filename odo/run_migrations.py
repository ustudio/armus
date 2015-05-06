import os
import re


migration_filter = re.compile('migration_[0-9]{14}.*')


def extract_version(name):
    try:
        version = int(name.split("_")[1])
        return version
    #TODO make this more accurate
    except ValueError:
        return None


def get_migration_versions(path):
    migration_files = [filename for filename in os.listdir(path) if migration_filter.match(filename)]
    versions = [extract_version(filename) for filename in migration_files]

    return sorted(versions)
