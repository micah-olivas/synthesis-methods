"""The SynthesisMethod data model.

A method is described by a TOML file with four sections: ``[meta]`` (name, vendor,
type, when the data was collected), ``[capabilities]`` (sequence-length and
library-size limits), ``[simulation]`` (error rate and, for pooled methods, the
Q90/Q10 abundance skew), and ``[pricing]``. This class parses that structure; it does
not compute cost, which is left to the caller.
"""
from __future__ import annotations


class SynthesisMethod:
    """A synthesis method loaded from a TOML config file."""

    __slots__ = (
        "name", "vendor", "type", "date_collected", "notes",
        "seq_length_min", "seq_length_max",
        "library_size_min", "library_size_max",
        "error_rate", "skew_q90_q10",
        "pricing", "slug",
    )

    def __init__(self, slug, data):
        meta = data["meta"]
        caps = data["capabilities"]
        sim = data["simulation"]

        self.slug = slug
        self.name = meta["name"]
        self.vendor = meta["vendor"]
        self.type = meta["type"]
        self.date_collected = meta["date_collected"]
        self.notes = meta.get("notes", "")

        self.seq_length_min = caps["seq_length_min"]
        self.seq_length_max = caps["seq_length_max"]
        self.library_size_min = caps.get("library_size_min")
        self.library_size_max = caps.get("library_size_max")

        er = sim.get("error_rate", [1e-4, 5e-4])
        if len(er) == 1:
            er = [er[0], er[0]]
        self.error_rate = tuple(er)

        # skew_q90_q10 is the Q90/Q10 abundance ratio, meaningful only for pooled synthesis.
        if meta["type"] == "pooled":
            self.skew_q90_q10 = float(sim["skew_q90_q10"])
        else:
            self.skew_q90_q10 = None

        self.pricing = data["pricing"]

    def __repr__(self):
        return f"SynthesisMethod({self.slug!r}, {self.name!r})"
