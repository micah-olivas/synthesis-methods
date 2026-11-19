"""synthesis_methods: a shared registry of DNA-synthesis method definitions.

A small, dependency-light package (TOML plus a data model) that both `usortm` and
`library_designer` read, so vendor capabilities, limits, and pricing live in one
place. Cost and skew computation is left to the caller.

    from synthesis_methods import load_all_methods, get_method, find_methods

    m = get_method("twist_oligo_pools")
    m.type, m.seq_length_max            # "pooled", 350
    find_methods(seq_length=250, method_type="pooled")
"""
from __future__ import annotations

from .loader import (
    METHODS_DIR,
    find_methods,
    get_method,
    load_all_methods,
    load_method,
    platform_type,
    user_methods_dirs,
)
from .model import SynthesisMethod

__version__ = "0.1.0"
__all__ = [
    "SynthesisMethod",
    "load_method",
    "load_all_methods",
    "get_method",
    "find_methods",
    "platform_type",
    "user_methods_dirs",
    "METHODS_DIR",
    "__version__",
]
