from pkg_resources import working_set
from warnings import warn


def package_is_installed(package:str) -> bool:
    for i in working_set:
        if package == i.key:
            return True
    return False


def warn_if_missing(package:str):
    if not package_is_installed(package):
        warn(f"{package} is not installed", source=__package__)