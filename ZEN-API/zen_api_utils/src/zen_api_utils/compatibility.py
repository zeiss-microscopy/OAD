"""Feature-scoped diagnostics for generated client and ZEN server capabilities."""

from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from dataclasses import fields, is_dataclass
from functools import wraps
from importlib.metadata import PackageNotFoundError, version
from inspect import getattr_static

from grpclib.const import Status
from grpclib.exceptions import GRPCError


def _installed_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "unknown (distribution metadata unavailable)"


class ZenApiCompatibilityError(RuntimeError):
    """A required generated API capability or server RPC is unavailable.

    Attributes:
        feature (str): Utility feature that could not be used.
        detail (str): Missing capability or unsupported server RPC.
    """

    def __init__(self, feature: str, detail: str) -> None:
        self.feature = feature
        self.detail = detail
        super().__init__(
            f"ZEN API compatibility error for '{feature}': {detail}. "
            f"Installed distributions: zen_api={_installed_version('zen_api')}; "
            f"zen_api_utils={_installed_version('zen_api_utils')}. "
            "Install a compatible zen_api/zen_api_utils wheel pair declared by the utility release "
            "and run 'python -m pip check'. For unsupported server RPCs, use a ZEN installation "
            "that supports the requested feature."
        )


def _check_capabilities(
    feature: str, target: object, members: tuple[str, ...], methods: tuple[str, ...]
) -> None:
    missing = object()
    field_names = (
        {item.name for item in fields(target)} if is_dataclass(target) else set()
    )
    unavailable = [
        name
        for name in members
        if name not in field_names and getattr_static(target, name, missing) is missing
    ]
    unavailable.extend(
        name for name in methods if not callable(getattr(target, name, None))
    )
    if unavailable:
        target_type = target if isinstance(target, type) else type(target)
        target_name = f"{target_type.__module__}.{target_type.__qualname__}"
        raise ZenApiCompatibilityError(
            feature,
            f"missing required capability on {target_name}: {', '.join(unavailable)}",
        )


@contextmanager
def api_capabilities(
    feature: str,
    target: object | None = None,
    *,
    members: tuple[str, ...] = (),
    methods: tuple[str, ...] = (),
) -> Iterator[None]:
    """Guard API imports or a focused RPC call without masking unrelated errors.

    Args:
        feature (str): User-facing name of the utility feature.
        target (object | None): Client, message, or generated type to inspect.
        members (tuple[str, ...]): Required attributes or dataclass fields.
        methods (tuple[str, ...]): Required callable client methods.

    Raises:
        ZenApiCompatibilityError: An API import, required capability, or server
            RPC is unavailable. Import and RPC failures retain their cause.
        ValueError: Member or method checks were requested without a target.

    Notes:
        This checks presence, not wire or behavioral compatibility. Other import
        errors, RPC statuses, and programming errors propagate unchanged.
    """
    if target is None and (members or methods):
        raise ValueError(
            "A capability-check target is required for member or method checks."
        )
    if target is not None:
        _check_capabilities(feature, target, members, methods)
    try:
        yield
    except ImportError as exc:
        if exc.name is None or not (
            exc.name == "zen_api" or exc.name.startswith("zen_api.")
        ):
            raise
        raise ZenApiCompatibilityError(feature, str(exc)) from exc
    except GRPCError as exc:
        if exc.status != Status.UNIMPLEMENTED:
            raise
        raise ZenApiCompatibilityError(
            feature, f"ZEN server returned UNIMPLEMENTED: {exc.message}"
        ) from exc


def api_operation[**Parameters, Result](
    feature: str,
    target: object | None = None,
    *,
    members: tuple[str, ...] = (),
    methods: tuple[str, ...] = (),
) -> Callable[
    [Callable[Parameters, Awaitable[Result]]], Callable[Parameters, Awaitable[Result]]
]:
    """Apply capability diagnostics to an async utility operation.

    Args:
        feature (str): User-facing name of the utility operation.
        target (object | None): Generated type to check before calling the function.
        members (tuple[str, ...]): Required attributes or dataclass fields.
        methods (tuple[str, ...]): Required callable client methods.

    Returns:
        Callable: Decorator retaining the function's signature and return value.

    Notes:
        Errors deliberately handled inside the function retain their existing
        fallback behavior. Cancellation and unrelated exceptions propagate.
    """

    def decorate(
        function: Callable[Parameters, Awaitable[Result]],
    ) -> Callable[Parameters, Awaitable[Result]]:
        @wraps(function)
        async def guarded(
            *args: Parameters.args, **kwargs: Parameters.kwargs
        ) -> Result:
            with api_capabilities(feature, target, members=members, methods=methods):
                return await function(*args, **kwargs)

        return guarded

    return decorate
