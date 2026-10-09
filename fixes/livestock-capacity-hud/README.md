# Livestock Capacity HUD

Original standalone BinyamFS add-on, version 1.0.0.1. Install `builds/FS25_z_LivestockCapacityHUD.zip` alongside your livestock trailer and enable it in the save's mod list.

Adds animal count, current capacity and percentage to the existing game capacity HUD. Counts real animal clusters rather than visible models. Reads the trailer's live capacity, including Livestock Trailer Custom settings. Empty trailers show the largest supported type capacity; native trailers with different capacities per type change capacity when loaded.

Rejects a different animal **type** while the trailer is occupied and shows the red warning “Trailer already loaded with another animal type!” Different breeds within one type remain allowed; FS25 goats are sheep breeds. Empty the trailer to change type. The warning is throttled to prevent flooding during capacity queries.

The guard checks normal animal-dialog loading actions before native transfer callbacks. Read-only support and capacity queries remain unchanged so they cannot invalidate the animal list or issue warnings during opening. It does not silently discard animals in `addCluster`, modify saved animals, or repair existing mixed loads. Nonstandard transfer mods that bypass the animal dialog require separate review. This is not a server-side guard against custom transfer events.

## Validation

Lua 5.1 regression checks cover mixed breeds, different-type rejection despite a 5,000-capacity override, empty unlock, warning throttle, live capacity changes and integer HUD text. GIANTS TestRunner results are recorded in `validation/`. User screenshot confirms Animals — 1,460 / 5,000 (29%) with the native capacity bar. Version 1.0.0.0 subsequently caused an animal-dialog regression during opening; 1.0.0.1 removes the dynamic type filtering and capacity rejection during browsing. The corrected dialog and transfer warning still need in-game confirmation.

Build with Python and Pillow: `python build.py`. Run behavior tests with Lua 5.1 through Lupa: `python test.py`.

GPL-3.0-or-later. Copyright 2026 BinyamFS. This folder contains original add-on code and generated artwork, with no third-party trailer or capacity-mod files.
