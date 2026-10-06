# Bees Revamp repairs and compatibility history

This supplements the original [honey inspection](Inspection.md) and [toggle repair notes](Repair-notes.md). It covers the earlier FS25 hive-system and proximity display work as well as honey output. Original mod author: Peppie84. No complete mod, source archive or assets are distributed.

## Evidence and versions

The retained source captured during the 22 September 2026 inspection already contained the earlier compatibility repairs while still reporting 1.0.1.0. Thus the version number alone does not distinguish an untouched author build from that local patched build. The active Alma build reports 1.0.1.4. Earlier compatibility behavior is reconstructed from that retained source and corroborated by the Game Crash Report conversation, which reported working hive recognition, bee counts and proximity infoboxes before investigating honey.

The original standalone report for those earlier repairs has not been located among the currently recovered files. This document is a reconstruction, not a claim to reproduce that missing report verbatim. The recovered Inspection.md and Repair-notes.md are the earlier supplied reports available locally.

## 1. Mission loading and hive-system identity

Files: `src/main.lua`, `src/beehivesystemextended.lua`.

The early load hook stores metadata rather than replacing a system before the game creates its own. An appended `Mission00.load` hook upgrades the engine-created system after creation. `BeehiveSystemExtended.upgradeExisting` copies extension methods onto the existing instance, retaining its identity and stock metatable. This preserves references, registered hives, spawners and callbacks held by other systems. If no stock system exists, a defensive fallback creates the extension.

The upgrade deliberately excludes `updateState` and `delete`, preserving current FS25 state handling and lifecycle. It initializes the field-info extension and refreshes state. The old development state implementation could leave FX disabled on current FS25 builds. The successful upgrade is logged.

## 2. Third-party hive specialization and initial state

Files: `src/main.lua`, `src/beecare.lua`.

Placeable types are patched again after mission loading so late-registered third-party hives receive BeeCare and the extended hive specialization. A one-time first-live-update refresh applies the upgraded system state to each hive's stock sound, FX and production flags after savegame placeables have loaded.

These repair lifecycle/registration compatibility. They do not bypass normal honey maturity, nectar or zero-population conditions.

## 3. Proximity infobox selection and idle hives

Files: `src/main.lua`, `src/beecare.lua`.

Placeable updates are demand-driven and do not reliably detect a player approaching an idle hive. A mission-level runtime listener polls proximity selection every 250 ms. `BeeCare.updateFallbackInfoSelection` selects the nearest eligible registered hive within five metres, makes its info trigger/drawable visible, and hides/removes the previously selected hive when the player moves away or another hive becomes closest. Cleanup clears the selected hive when removed.

The information chain includes colony state, population, swarm information, nectar and colony count, while retaining the overwritten info function. The recovered conversation reported the hive recognition/count/proximity side working. This does not establish honey output.

## 4. Multifruit compatibility and tuning

File: `src/main.lua`.

The retained earlier compatibility source explicitly adds HEMP and CLOVER to its bee-yield patch list with a 0.10 bonus and one hive per hectare, identified in its comments as Glenleathann/multifruit compatibility. These are local crop compatibility/balance choices, not universal defaults and not a new fix for every crop. Existing upstream colony-count tables, population simulation, price behavior and other crop bonuses must not be attributed automatically to our repairs.

## 5. Honey investigation and optional output mode

The recovered [Inspection.md](Inspection.md) explains why living animated young colonies can legitimately produce zero honey, and distinguishes this from accounting defects in elapsed time and nectar scaling. Its unconditional vanilla-delegation compatibility patch was superseded by the optional toggle.

Repair versions 1.0.1.1 through 1.0.1.4 add save-local mode persistence, host/client synchronization, menu integration, non-recursive control refresh, regular elapsed-time collection, timestamp resets on mode changes and production telemetry. See [Repair-notes.md](Repair-notes.md) for exact touched files and behavior.

## 6. Later in-game confirmation

The recovered 22 September 2026 repair chat contains the user's explicit On -> Off -> On test: honey spawned, stopped and resumed. The accompanying log review reported 312 active hive installations, no missing spawners or pallet-limit flags, resumed production after toggling, and no Lua errors. This is later evidence than the original README's statement that gameplay confirmation was still required.

The 2 October log audit also records active-hive output telemetry and increased production after toggling without an accompanying exception. These support the tested configuration; exhaustive multiplayer, other mods and physical spawn-clearance scenarios remain outside the evidence. Automated tests described in the older report were not rerun for this documentation update.

## Separate honey-spawn utility

Faster Honey Pallet Cadence changes the materialization schedule of honey pallets, not Bees Revamp's colony/nectar model. It is maintained as its own utility in [FS25-Mods](https://github.com/binyamfs-alt/FS25-Mods). Do not conflate that work with this repair history.
