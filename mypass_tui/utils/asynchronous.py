import inspect
from typing import Awaitable, Callable, TypeVar, Union

T = TypeVar("T")


async def await_me_maybe(callback: Callable[..., Union[T, Awaitable[T]]], *args, **kwargs) -> Union[T, Awaitable[T]]:
    result = callback(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result
