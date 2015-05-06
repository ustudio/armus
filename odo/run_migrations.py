import os


def _extract_version(name):
    try:
        version = int(name.split("_")[1])
        return version
    except ValueError:
        return None
    raise


def _all_versions(path):
    versions = set()
    for directory_info in os.walk(path):
        # tuple index 2 is the list of filenames
        for filename in directory_info[2]:
            version = _extract_version(filename)
            if version:
                versions.add(version)
    return versions


path = os.path.abspath(os.path.join(os.path.abspath(__file__), '../..', 'migrations'))

print _all_versions(path)
