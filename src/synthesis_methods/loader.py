"""Load and query the bundled synthesis-method registry."""
from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from .model import SynthesisMethod

METHODS_DIR = Path(__file__).parent / "data" / "methods"


def load_method(path) -> SynthesisMethod:
    """Load a single method from a TOML file."""
    path = Path(path)
    with open(path, "rb") as f:
        return SynthesisMethod(path.stem, tomllib.load(f))


def load_all_methods(methods_dir=None) -> dict:
    """All methods as a dict keyed by slug. Reads the bundled registry unless
    ``methods_dir`` points elsewhere."""
    d = Path(methods_dir) if methods_dir else METHODS_DIR
    return {m.slug: m for m in (load_method(p) for p in sorted(d.glob("*.toml")))}


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
