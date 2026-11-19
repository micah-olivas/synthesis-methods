"""Load and query the bundled synthesis-method registry."""
from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from .model import SynthesisMethod

METHODS_DIR = Path(__file__).parent / "data" / "methods"
ENV_VAR = "SYNTHESIS_METHODS_PATH"


def load_method(path) -> SynthesisMethod:
    """Load a single method from a TOML file."""
    path = Path(path)
    with open(path, "rb") as f:
        return SynthesisMethod(path.stem, tomllib.load(f))


def user_methods_dirs() -> list:
    """Extra method directories read after the bundled registry: each entry of
    ``SYNTHESIS_METHODS_PATH`` (``os.pathsep``-separated), then
    ``~/.config/synthesis-methods/methods`` if it exists. These hold method
    definitions that are not distributed with the package, such as quoted
    pricing."""
    dirs = [Path(p).expanduser() for p in os.environ.get(ENV_VAR, "").split(os.pathsep) if p]
    default = Path.home() / ".config" / "synthesis-methods" / "methods"
    if default.is_dir():
        dirs.append(default)
    return dirs


def load_all_methods(methods_dir=None) -> dict:
    """All methods as a dict keyed by slug. With no ``methods_dir``, reads the
    bundled registry, then each of ``user_methods_dirs()``; a later file
    replaces an earlier one with the same slug. With ``methods_dir``, reads
    only that directory."""
    dirs = [Path(methods_dir)] if methods_dir else [METHODS_DIR, *user_methods_dirs()]
    methods = {}
    for d in dirs:
        for p in sorted(d.glob("*.toml")):
            m = load_method(p)
            methods[m.slug] = m
    return methods


def get_method(slug, methods_dir=None) -> SynthesisMethod:
    """One method by slug (e.g. ``"twist_oligo_pools"``)."""
    methods = load_all_methods(methods_dir)
    try:
        return methods[slug]
    except KeyError:
        raise KeyError(f"Unknown synthesis method {slug!r}; known: {sorted(methods)}") from None


def find_methods(seq_length, library_size=None, method_type=None, methods_dir=None):
    """Methods whose capabilities cover the given sequence length (and, if given,
    library size and type). Returns a list of SynthesisMethod objects."""
    results = []
    for method in load_all_methods(methods_dir).values():
        if method_type and method.type != method_type:
            continue
        if not (method.seq_length_min <= seq_length <= method.seq_length_max):
            continue
        if (
            library_size is not None
            and method.library_size_min is not None
            and method.library_size_max is not None
            and not (method.library_size_min <= library_size <= method.library_size_max)
        ):
            continue
        results.append(method)
    return results


def platform_type(platform, methods_dir=None) -> str:
    """Resolve a platform to ``"pooled"`` or ``"arrayed"``. The two type names pass
    through unchanged; any other value is looked up as a method slug."""
    if platform in ("pooled", "arrayed"):
        return platform
    return get_method(platform, methods_dir).type
