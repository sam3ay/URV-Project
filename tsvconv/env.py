import os


def set_env(variable_name, value):
    """Add variable to environment

    Args:
        variable_name (str): Name of variable
        value : being assigned to variable

    Returns:
        Environmental variable

    Example:
    >>> os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
    """
    os.environ[variable_name] = value


def unset_env(variable_name):
    """Remove environmental variable

    Args:
        variable_name (str): Name of variable

    Returns:
        Removes environmental variable and updates os.environ

    Raises:
        KeyError: When variable_name is not in environ
    Notes:
        del is prefereable to unsetenv because it also updates os.environ;
        see unsetenv documentation
    """
    del os.environ[variable_name]
