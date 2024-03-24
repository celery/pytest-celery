"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

from __future__ import annotations

import time
from typing import Any
from typing import Iterable

import celery.utils
from celery import Task
from celery import shared_task


# ------------- add -------------
@shared_task
def add(x: int | float, y: int | float, z: int | float | None = None) -> int | float:
    """Pytest-celery internal task.

    This task adds two or three numbers together.

    Args:
        x (int | float): The first number.
        y (int | float): The second number.
        z (int | float | None, optional): The third number. Defaults to None.

    Returns:
        int | float: The sum of the numbers.
    """
    if z:
        return x + y + z
    else:
        return x + y


# ------------- add_replaced -------------
@shared_task(bind=True)
def add_replaced(
    self: Task,
    x: int | float,
    y: int | float,
    z: int | float | None = None,
    *,
    queue: str | None = None,
) -> None:
    """Pytest-celery internal task.

    This task replaces itself with the add task for the given arguments.

    Args:
        x (int | float): The first number.
        y (int | float): The second number.
        z (int | float | None, optional): The third number. Defaults to None.

    Raises:
        Ignore: Always raises Ignore.
    """
    queue = queue or "celery"
    raise self.replace(add.s(x, y, z).set(queue=queue))


# ------------- fail -------------
@shared_task
def fail(*args: tuple) -> None:
    """Pytest-celery internal task.

    This task raises a RuntimeError with the given arguments.

    Args:
        *args (tuple): Arguments to pass to the RuntimeError.

    Raises:
        RuntimeError: Always raises a RuntimeError.
    """
    args = (("Task expected to fail",) + args,)
    raise RuntimeError(*args)


# ------------- identity -------------
@shared_task
def identity(x: Any) -> Any:
    """Pytest-celery internal task.

    This task returns the input as is.

    Args:
        x (Any): Any value.

    Returns:
        Any: The input value.
    """
    return x


# ------------- noop -------------
@shared_task
def noop(*args: tuple, **kwargs: dict) -> None:
    """Pytest-celery internal task.

    This is a no-op task that does nothing.

    Returns:
        None: Always returns None.
    """
    return celery.utils.noop(*args, **kwargs)


# ------------- ping -------------
@shared_task
def ping() -> str:
    """Pytest-celery internal task.

    Used to check if the worker is up and running.

    Returns:
        str: Always returns "pong".
    """
    return "pong"


# ------------- sleep -------------
@shared_task
def sleep(seconds: float = 1, **kwargs: dict) -> bool:
    """Pytest-celery internal task.

    This task sleeps for the given number of seconds.

    Args:
        seconds (float, optional): The number of seconds to sleep. Defaults to 1.
        **kwargs (dict): Additional keyword arguments.

    Returns:
        bool: Always returns True.
    """
    time.sleep(seconds, **kwargs)
    return True


# ------------- xsum -------------
@shared_task
def xsum(nums: Iterable) -> int:
    """Pytest-celery internal task.

    This task sums a list of numbers, but also supports nested lists.

    Args:
        nums (Iterable): A list of numbers or nested lists.

    Returns:
        int: The sum of the numbers.
    """
    return sum(sum(num) if isinstance(num, Iterable) else num for num in nums)
