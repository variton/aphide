"""envvar_loader module."""

def load(envvar:str=None) -> str|None:
    """function to load env var."""
    try:
        return __import__("os").environ["SJWTK"] if envvar is None else __import__("os").environ[envvar]
    except KeyError as e:
        return None
