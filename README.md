# synthesis-methods

A shared registry of DNA-synthesis method definitions: vendor capabilities, sequence-length and library-size limits, error and skew estimates, and pricing. Each method is a TOML file parsed into a small `SynthesisMethod` model. Both `usortm` and `library_designer` read from here, so the numbers live in one place instead of being copied between tools.

This package holds the data and the loader. It does not compute cost; a caller that needs cost (uSort-M) reads `method.pricing` and does its own math.

## Use

```python
from synthesis_methods import load_all_methods, get_method, find_methods, platform_type

methods = load_all_methods()                 # {slug: SynthesisMethod}
m = get_method("twist_oligo_pools")
m.type, m.seq_length_min, m.seq_length_max   # "pooled", 20, 350
find_methods(seq_length=250, method_type="pooled")
platform_type("idt_eblocks")                 # "arrayed"
```

## Adding or editing a method

Add a TOML file under `src/synthesis_methods/data/methods/`, keyed by its filename slug. Each file has four sections: `[meta]`, `[capabilities]`, `[simulation]`, and `[pricing]`. Copy an existing file for the shape. Provenance for the pricing and capability numbers lives in `data/methods/sources/`.
