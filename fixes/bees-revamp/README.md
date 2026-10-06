# Bees Revamp optional vanilla honey repair

Original mod author: Peppie84. Original inspected version: 1.0.1.0. Local compatibility repair: 1.0.1.4. [Detailed repair and test notes](Repair-notes.md) record the completed work. The original or modified mod is not distributed here.

## Problem and behavior

Young-colony and nectar gates can explain no honey despite visible bees. A separate General Settings refresh bug in repair 1.0.1.1 forced recursive callbacks and a stack overflow. The later repair provides an optional vanilla honey mode and fixes that menu recursion; it does not claim to repair the complete realism model.

Off is the default and preserves the original output scheduling and colony/nectar rules. On delegates honey calculation to the stock elapsed-time path and polls the existing hive output once per second on the server. Ordinary production conditions and the nonpositive-population shutoff still apply. Honey generation in this mode does not consume nectar.

## Change recipe

For an authorized local reconstruction from the matching original, the documented change set is:

- Add a separate settings module at `src/honeysettings.lua` for save-local persistence, host/client synchronization, menu integration and regular output polling.
- In `src/main.lua`, source and initialize that module, load its save state, and call its output update from the existing update path.
- In `PlaceableBeehiveExtended:getHoneyAmountToSpawn` in `src/placeablebeehiveextended.lua`, delegate to the existing `superFunc` chain only when vanilla honey mode is enabled; otherwise retain the original conversion.
- Refresh the settings control using `setState(value, false)` so refresh does not force another callback. Reset elapsed-time markers when switching modes.
- Update only the local repair version in `modDesc.xml` to 1.0.1.4.

This recipe records design and touch points, not a complete executable patch. Full third-party source and a redistribution patch are intentionally absent.

## Use an already repaired local copy

Back up the mod and save and close FS25. Retain `FS25_z_BeesRevamp.zip` and install only one copy. In General Settings, find Bees Revamp: vanilla honey production. On is a save-wide host-controlled option. Save to persist it in `beesRevampHoneySettings.xml`. Clients receive the host state. See the detailed notes for the stopped dedicated-server XML option.

## Validation and rollback

Reproduce with a living hive and an owned unobstructed spawner during active production. Check accrued litres, not only whether a full pallet appears. Repeated collection at identical game time should yield zero additional honey. Check menu opening, mode changes, reload persistence and the per-minute output summary. Stock spawner clearance, pallet limits and the actual Lazy Distribution trigger still require live end-to-end checks.

Recorded automated tests cover Lua compilation, toggle behavior, time accounting, menu callbacks, persistence and network serialization, plus stock SDK pipeline simulation. Those are historical test results, not tests rerun when publishing these notes. Restore the backed-up ZIP to undo the repair; preserve or restore the save backup as appropriate.

## Current local fingerprint

On 6 October 2026, the active Alma ZIP reported 1.0.1.4 and contained the conditional vanilla delegation, settings integration, one-second polling and non-recursive menu refresh. SHA-256: `E8BCC3CC39CED2EF3BA5169AE1D8387BBB528A37666003A21E3944EA27EA0909`.

This records the inspected local build only; it is not an upstream checksum or proof of compatibility with later releases.
