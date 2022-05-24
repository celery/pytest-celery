try:
    from functools import cached_property
except ImportError:
    # TODO: Remove this backport once we drop Python 3.7 support
    from cached_property import cached_property

