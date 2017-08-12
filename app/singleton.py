"""
@breif: singleton base class
@author: vikadoo
@version: $id
"""


class Singleton(object):
    """
    simple singleton
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
