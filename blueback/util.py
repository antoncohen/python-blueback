import os

class ObjectDict(dict):
    """Makes a dictionary behave like an object."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def expand_paths(paths):
    fullpaths = []
    for i in paths:
        path = os.path.expanduser(i)
        fullpaths.append(path)

    return fullpaths
