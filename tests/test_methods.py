from __future__ import annotations

import pytest

from synthesis_methods import (
    METHODS_DIR,
    SynthesisMethod,
    find_methods,
    get_method,
    load_all_methods,
    platform_type,
    user_methods_dirs,
)


@pytest.fixture
def no_user_dirs(tmp_path, monkeypatch):
    """Isolate from the developer's own ~/.config and SYNTHESIS_METHODS_PATH."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("SYNTHESIS_METHODS_PATH", raising=False)
    return tmp_path


def test_load_all_methods(no_user_dirs):
    methods = load_all_methods()
    assert {"idt_eblocks", "idt_gblocks", "twist_oligo_pools",
            "twist_multiplexed_gene_fragments"} <= set(methods)
    assert all(isinstance(m, SynthesisMethod) for m in methods.values())
    assert all(slug == m.slug for slug, m in methods.items())


def _write_method(d, slug, name):
    d.mkdir(parents=True, exist_ok=True)
    src = (METHODS_DIR / "idt_eblocks.toml").read_text()
    (d / f"{slug}.toml").write_text(src.replace('name = "IDT eBlocks"', f'name = "{name}"'))


def test_user_dirs_add_and_override(no_user_dirs, monkeypatch):
    env_dir = no_user_dirs / "env"
    default_dir = no_user_dirs / "home" / ".config" / "synthesis-methods" / "methods"
    _write_method(env_dir, "quoted_method", "Quoted")
    _write_method(default_dir, "idt_eblocks", "Overridden")
    monkeypatch.setenv("SYNTHESIS_METHODS_PATH", str(env_dir))

    assert user_methods_dirs() == [env_dir, default_dir]
    methods = load_all_methods()
    assert methods["quoted_method"].name == "Quoted"
    assert methods["idt_eblocks"].name == "Overridden"
    # an explicit methods_dir reads only that directory
    assert set(load_all_methods(env_dir)) == {"quoted_method"}


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
