# Livestock Capacity HUD

Original standalone BinyamFS add-on, version 1.0.0.0. Install `builds/FS25_z_LivestockCapacityHUD.zip` alongside your livestock trailer and enable it in the save's mod list.

Adds animal count, current capacity and percentage to the existing game capacity HUD. Counts real animal clusters rather than visible models. Reads the trailer's live capacity, including Livestock Trailer Custom settings. Empty trailers show the largest supported type capacity; native trailers with different capacities per type change capacity when loaded.

Rejects a different animal **type** while the trailer is occupied and shows the red warning “Trailer already loaded with another animal type!” Different breeds within one type remain allowed; FS25 goats are sheep breeds. Empty the trailer to change type. The warning is throttled to prevent flooding during capacity queries.

The guard wraps native support/capacity checks before animal transfers. It does not silently discard animals in `addCluster`, modify saved animals, or repair existing mixed loads. Nonstandard transfer mods that bypass native support/capacity checks require separate review.

## Validation

Lua 5.1 regression checks cover mixed breeds, different-type rejection despite a 5,000-capacity override, empty unlock, warning throttle, live capacity changes and integer HUD text. GIANTS TestRunner results are recorded in `validation/`. Actual in-game HUD placement and animal transfer confirmation remain pending user testing; packaging checks do not confirm gameplay.

Build with Python and Pillow: `python build.py`. Run behavior tests with Lua 5.1 through Lupa: `python test.py`.

GPL-3.0-or-later. Copyright 2026 BinyamFS. This folder contains original add-on code and generated artwork, with no third-party trailer or capacity-mod files.
