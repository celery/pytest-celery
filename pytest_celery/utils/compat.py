import typing

try:
    list[object]
except AttributeError:
    List = typing.List
else:
    List = list

__all__ = ('List',)
