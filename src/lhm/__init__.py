"""Core package for the LHM data platform."""

from importlib import resources


def get_version() -> str:
    """Return the package version if metadata is available.

    The skeleton package does not yet ship with a build system that
    automatically injects version metadata. The helper gracefully
    falls back to ``"0.0.0"`` so that downstream modules have a
    reliable semantic version string to reference during early
    development.
    """

    try:
        with resources.files(__package__).joinpath("VERSION").open("r", encoding="utf-8") as handle:
            return handle.read().strip()
    except FileNotFoundError:
        return "0.0.0"
