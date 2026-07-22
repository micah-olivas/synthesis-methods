# synthesis-methods

A shared registry of commercial DNA synthesis method definitions: vendor capabilities, sequence-length and library-size limits, error and skew estimates, and pricing. Each method is a TOML file parsed into a small `SynthesisMethod` model.

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
