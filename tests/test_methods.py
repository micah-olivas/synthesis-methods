from __future__ import annotations

import pytest

from synthesis_methods import (
    SynthesisMethod,
    find_methods,
    get_method,
    load_all_methods,
    platform_type,
)


def test_load_all_methods():
    methods = load_all_methods()
    assert len(methods) >= 8
    assert all(isinstance(m, SynthesisMethod) for m in methods.values())
    assert all(slug == m.slug for slug, m in methods.items())


def test_known_method_fields():
    m = get_method("twist_oligo_pools")
    assert m.type == "pooled"
    assert m.seq_length_min == 20 and m.seq_length_max == 350
    assert m.skew_q90_q10 == 4.0            # pooled methods carry a skew
    assert m.pricing["model"] == "lookup"


def test_arrayed_method_has_no_skew():
    m = get_method("idt_eblocks")
    assert m.type == "arrayed"
    assert m.skew_q90_q10 is None


def test_platform_type():
    assert platform_type("pooled") == "pooled"
    assert platform_type("arrayed") == "arrayed"
    assert platform_type("twist_oligo_pools") == "pooled"
    assert platform_type("idt_eblocks") == "arrayed"


def test_find_methods_filters():
    hits = find_methods(seq_length=250, method_type="pooled")
    assert hits and all(m.type == "pooled" for m in hits)
    assert any(m.slug == "twist_oligo_pools" for m in hits)
    # a length no method supports returns nothing
    assert find_methods(seq_length=10_000) == []


def test_unknown_method_raises():
    with pytest.raises(KeyError):
        get_method("does_not_exist")
